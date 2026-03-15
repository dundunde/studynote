
import os
import numpy as np
# 在所有依赖于 Bokeh 或 Backtrader 的 import 之前，强行打个补丁
if not hasattr(np, 'bool8'):
    np.bool8 = np.bool_
if not hasattr(np, 'object'):
    np.object = object
if not hasattr(np, 'float'):
    np.float = float
if not hasattr(np, 'int'):
    np.int = int
os.environ["BOKEH_RESOURCES"] = "inline"
from bokeh.resources import INLINE, Resources
# print(Resources().mode)

import sys
import ccxt
import datetime
import pandas as pd
import quantstats as qs
import backtrader as bt

from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo
from collections import deque



import backtrader as bt
import numpy as np
import math

class CryptoMomentumRotation(bt.Strategy):
    """
    加密货币多因子动量轮动策略 (复刻原版策略3：七星ETF轮动)
    核心逻辑：MA20趋势过滤 + RSI超买过滤 + 动量加权打分(年化收益*R²) + 换仓缓冲区
    """
    params = dict(
        # 基础参数
        hold_num=3,               # 目标持仓数量 (原策略为5只，加密市场相关性高，建议3-5只)
        buffer_top_n=5,           # 换仓缓冲区 (原策略为8，如果老持仓掉到第4、5名暂不卖出减少磨损)
        
        # 动量计算参数
        lookback_days=25,         # 长期动量周期
        min_score=1.0,            # 入选最低得分
        
        # 过滤开关与参数
        enable_ma_filter=True,    # 是否开启均线趋势过滤 (必须站上MA20)
        ma_period=20,             
        
        use_rsi=True,             # RSI超买过滤
        rsi_period=6,
        rsi_threshold=98,
        
        enable_volume=True,       # 高位放量过滤
        vol_lookback=5,
        vol_threshold=1.5,        # 放量倍数
        
        short_momentum=True,      # 短期动量过滤
        short_days=10,
        short_threshold=0.0
    )

    def __init__(self):
        self.inds = {}
        # 为每一个传入的数据集(币种)初始化独立指标
        for d in self.datas:
            self.inds[d._name] = {
                'ma20': bt.indicators.SMA(d.close, period=self.p.ma_period),
                'ma5': bt.indicators.SMA(d.close, period=5),
                'rsi': bt.indicators.RSI_Safe(d.close, period=self.p.rsi_period),
                'vol_sma': bt.indicators.SMA(d.volume, period=self.p.vol_lookback)
            }

    def prenext(self):
        # 等待所有数据准备好
        self.next()

    def calc_momentum_score(self, d):
        """计算单币种的动量得分及过滤"""
        # 1. 获取近期价格数据
        prices = np.array(d.close.get(size=self.p.lookback_days))
        if len(prices) < self.p.lookback_days:
            return None

        current_price = d.close[0]
        inds = self.inds[d._name]

        # 2. 均线趋势过滤 (跌破MA20直接淘汰)
        if self.p.enable_ma_filter and current_price < inds['ma20'][0]:
            return None

        # 3. RSI超买过滤 (RSI极高且跌破MA5，视为高位走弱)
        if self.p.use_rsi:
            if inds['rsi'][0] > self.p.rsi_threshold and current_price < inds['ma5'][0]:
                return None

        # 4. 短期动量过滤 (近期10天不能是下跌趋势)
        if self.p.short_momentum:
            short_prices = np.array(d.close.get(size=self.p.short_days + 1))
            if len(short_prices) == self.p.short_days + 1:
                short_ret = short_prices[-1] / short_prices[0] - 1
                # Crypto按365天计算年化
                short_ann = (1 + short_ret) ** (365 / self.p.short_days) - 1
                if short_ann < self.p.short_threshold:
                    return None

        # 5. 急跌风控 (近3日不能有单日暴跌超3%，Crypto波动大，这里放宽或可调整为5-10%)
        if len(prices) >= 4:
            d1 = prices[-1] / prices[-2]
            d2 = prices[-2] / prices[-3]
            d3 = prices[-3] / prices[-4]
            if min(d1, d2, d3) < 0.90:  # 币圈建议调为单日跌幅超10%过滤
                return None

        # 6. 核心动量计算 (加权线性回归)
        # 给予近期数据更高权重
        y = np.log(prices)
        x = np.arange(len(y))
        weights = np.linspace(1, 2, len(y))
        
        slope, intercept = np.polyfit(x, y, 1, w=weights)
        annualized_returns = math.exp(slope * 365) - 1  # 币圈365天
        
        # 计算R² (拟合优度，衡量上涨的平滑性)
        ss_res = np.sum(weights * (y - (slope * x + intercept)) ** 2)
        ss_tot = np.sum(weights * (y - np.mean(y)) ** 2)
        r_squared = 1 - ss_res / ss_tot if ss_tot else 0

        # 动量得分 = 年化收益 * R²
        score = annualized_returns * r_squared

        # 7. 高位放量过滤 (如果年化收益高，且今日爆量，怀疑是诱多出货)
        if self.p.enable_volume and annualized_returns > 1.0: # 年化>100%视为高位
            avg_vol = inds['vol_sma'][-1]
            if avg_vol > 0 and (d.volume[0] / avg_vol) > self.p.vol_threshold:
                return None

        return score

    def next(self):
        # 如果还在准备期，跳过
        if len(self) < self.p.lookback_days:
            return

        # 1. 对所有池子中的币种进行打分排序
        scores = []
        for d in self.datas:
            score = self.calc_momentum_score(d)
            if score is not None and score > self.p.min_score:
                scores.append((score, d))
        
        # 按得分降序排序
        scores.sort(key=lambda x: x[0], reverse=True)
        ranked_datas = [x[1] for x in scores]
        valid_names = [d._name for d in ranked_datas]

        # 2. 确定目标持仓 (引入原策略的“换仓缓冲区 Buffer”逻辑)
        target_datas = []
        current_holdings = [d for d in self.datas if self.getposition(d).size > 0]
        
        # 2.1 优先保留在前 N (缓冲区) 名的老持仓，减少来回摩擦
        top_buffer_names = valid_names[:self.p.buffer_top_n]
        for d in current_holdings:
            if d._name in top_buffer_names and len(target_datas) < self.p.hold_num:
                target_datas.append(d)
                
        # 2.2 填充剩余空位 (从得分最高的开始填)
        for d in ranked_datas:
            if len(target_datas) >= self.p.hold_num:
                break
            if d not in target_datas:
                target_datas.append(d)

        target_names = [d._name for d in target_datas]

        # 3. 防御逻辑
        # 如果目标池为空，说明所有币种都跌破MA20或动量为负
        if not target_datas:
            self.log("【防御状态】全市场极弱，清仓持有现金 (USDT)")

        # 4. 执行调仓
        # 4.1 卖出不在目标列表中的持仓
        for d in current_holdings:
            if d._name not in target_names:
                self.close(d)
                self.log(f"平仓卖出: {d._name}")

        # 4.2 买入/调仓 目标列表中的币种
        if target_datas:
            # 等权分配资金
            target_percent = 1.0 / len(target_datas)
            for d in target_datas:
                self.order_target_percent(d, target=target_percent)
                self.log(f"目标持仓: {d._name}, 比例: {target_percent*100:.1f}%")

    def log(self, txt, dt=None):
        """简易日志输出"""
        dt = dt or self.datas[0].datetime.date(0)
        print(f'[{dt.isoformat()}] {txt}')


def run_backtest():
    # 1. 初始化 Cerebro 引擎
    cerebro = bt.Cerebro()

    # 2. 添加策略
    cerebro.addstrategy(CryptoMomentumRotation)
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')

    # 3. 定义你的加密货币资产池 (可以根据需要增减)
    # 这里选择市值靠前、流动性好的标的作为轮动池
    crypto_pool = [
        # ('BTCUSDT', '15m'),
        # ('BTCUSDT', '4h'),
        ('BTCUSDT', '1d'),
        # ('ETHUSDT', '15m'),
        # ('ETHUSDT', '4h'),
        ('ETHUSDT', '1d'),
        # ('SOLUSDT', '15m'),
        # ('SOLUSDT', '4h'),
        ('SOLUSDT', '1d'),
    ]
    
    # 回测时间范围：例如过去两年
    start_date = '2023-01-01'
    end_date = '2026-01-01'

    for key, value in crypto_pool:
        data_df = pd.read_csv(
            f"./quantify/data/{key}_{value}_2020_2026_Clean.csv",
            index_col='datetime',
            parse_dates=['datetime']
        )
        data_df = data_df.loc[start_date:end_date]

        data = bt.feeds.PandasData(
            dataname=data_df,
            datetime=None,  # None 表示直接使用 DataFrame 的索引 (即我们刚刚转换好的 DatetimeIndex)
            name=f'{key}',
            open='open',
            high='high',
            low='low',
            close='close',
            volume='volume',
            openinterest=-1 # 如果你的数据里没有持仓量列，设为 -1 表示忽略
        )
        cerebro.adddata(data=data)
        print(f"成功加载: {key} (数据量: {len(data_df)} 条)")

    # 4. 设置初始资金和手续费
    start_cash = 100000.0
    cerebro.broker.setcash(start_cash)
    
    # 币安等主流交易所现货手续费通常在 0.1% 左右
    cerebro.broker.setcommission(commission=0.001)

    # 5. 运行回测
    print('\n' + '='*50)
    print(f'初始资金: {start_cash:.2f} USDT')
    print('='*50)
    
    # 执行策略
    results = cerebro.run()

    # 6. 输出结果
    end_cash = cerebro.broker.getvalue()
    print('='*50)
    print(f'最终资金: {end_cash:.2f} USDT')
    print(f'总收益率: {((end_cash / start_cash) - 1) * 100:.2f}%')
    print('='*50)

    # 7. 绘制回测图表 (可选：如果你的环境支持弹窗)
    strat = results[0]
    b = Bokeh(style='bar', plot_mode='single', scheme=Tradimo(), use_cdn=False)
    cerebro.plot(b)

    # 6. 提取收益率数据
    portfolio_stats = strat.analyzers.getbyname('_TimeReturn')
    returns = portfolio_stats.get_analysis()

    # 7. 将字典转换为 pandas.Series，并将索引转为日期时间格式
    # 这一步是必须的，因为 QuantStats 只认 pandas 数据格式
    returns_series = pd.Series(returns)
    returns_series.index = pd.to_datetime(returns_series.index)
    
    # 由于时区问题，需要去掉时区信息（如果有的话），防止 QuantStats 报错
    returns_series.index = returns_series.index.tz_localize(None)

    # 8. 使用 QuantStats 生成网页版分析报告
    # 这会在你脚本的同级目录下生成一个 strategy_report.html 文件
    print("正在生成 QuantStats 报告...")
    qs.reports.html(returns_series, output='strategy_report.html', title='Oracle 策略回测报告')
    print("报告生成完毕！请在文件夹中双击打开 strategy_report.html")


if __name__ == '__main__':
    run_backtest()