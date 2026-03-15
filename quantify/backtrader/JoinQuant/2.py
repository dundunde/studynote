
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
    加密货币多因子动量轮动策略 (增加做空逻辑)
    核心逻辑：MA20趋势过滤 + RSI超买/超卖过滤 + 动量加权打分(年化收益*R²) + 换仓缓冲区
    """
    params = dict(
        # 基础参数
        hold_num=3,               # 单边目标持仓数量 (做多3只，做空3只)
        buffer_top_n=5,           # 换仓缓冲区
        allow_short=True,         # 做空总开关
        
        # 动量计算参数
        lookback_days=25,         # 长期动量周期
        min_score=1.0,            # 入选最低绝对得分 (做多需 > min_score, 做空需 < -min_score)
        
        # 过滤开关与参数
        enable_ma_filter=True,    # 均线趋势过滤 
        ma_period=20,             
        
        use_rsi=True,             # RSI极值过滤
        rsi_period=6,
        rsi_threshold=98,         # 做多超买过滤
        rsi_short_threshold=30,   # 做空超卖过滤 (避免在底部追空)
        
        enable_volume=True,       # 高位放量/低位爆量过滤
        vol_lookback=5,
        vol_threshold=1.5,        
        
        short_momentum=True,      # 短期动量过滤
        short_days=10,
        short_threshold=0.0
    )

    def __init__(self):
        self.inds = {}
        for d in self.datas:
            self.inds[d._name] = {
                'ma20': bt.indicators.SMA(d.close, period=self.p.ma_period),
                'ma5': bt.indicators.SMA(d.close, period=5),
                'rsi': bt.indicators.RSI_Safe(d.close, period=self.p.rsi_period),
                'vol_sma': bt.indicators.SMA(d.volume, period=self.p.vol_lookback)
            }

    def prenext(self):
        self.next()

    def calc_momentum_score(self, d):
        """计算单币种的动量得分，并返回信号类型 (1: 做多, -1: 做空, 0: 观望)"""
        prices = np.array(d.close.get(size=self.p.lookback_days))
        if len(prices) < self.p.lookback_days:
            return 0, 0

        current_price = d.close[0]
        inds = self.inds[d._name]

        # 计算核心动量 (加权线性回归)
        y = np.log(prices)
        x = np.arange(len(y))
        weights = np.linspace(1, 2, len(y))
        
        slope, intercept = np.polyfit(x, y, 1, w=weights)
        annualized_returns = math.exp(slope * 365) - 1 
        
        ss_res = np.sum(weights * (y - (slope * x + intercept)) ** 2)
        ss_tot = np.sum(weights * (y - np.mean(y)) ** 2)
        r_squared = 1 - ss_res / ss_tot if ss_tot else 0
        score = annualized_returns * r_squared

        # 准备短期数据用于过滤
        short_ann = 0.0
        if self.p.short_momentum:
            short_prices = np.array(d.close.get(size=self.p.short_days + 1))
            if len(short_prices) == self.p.short_days + 1:
                short_ret = short_prices[-1] / short_prices[0] - 1
                # 避免复数运算报错，加入安全处理
                short_ann = (1 + short_ret) ** (365 / self.p.short_days) - 1 if short_ret > -1 else -1

        d1 = d2 = d3 = 1.0
        if len(prices) >= 4:
            d1 = prices[-1] / prices[-2]
            d2 = prices[-2] / prices[-3]
            d3 = prices[-3] / prices[-4]
            
        avg_vol = inds['vol_sma'][-1]
        is_high_vol = self.p.enable_volume and avg_vol > 0 and (d.volume[0] / avg_vol) > self.p.vol_threshold

        # === 做多条件过滤 ===
        is_long = True
        if self.p.enable_ma_filter and current_price < inds['ma20'][0]: is_long = False
        if self.p.use_rsi and inds['rsi'][0] > self.p.rsi_threshold and current_price < inds['ma5'][0]: is_long = False
        if self.p.short_momentum and short_ann < self.p.short_threshold: is_long = False
        if min(d1, d2, d3) < 0.90: is_long = False  # 单日暴跌 > 10%
        if is_high_vol and annualized_returns > 1.0: is_long = False
        if score <= self.p.min_score: is_long = False

        if is_long: return score, 1

        # === 做空条件过滤 ===
        is_short = self.p.allow_short
        if self.p.enable_ma_filter and current_price > inds['ma20'][0]: is_short = False
        if self.p.use_rsi and inds['rsi'][0] < self.p.rsi_short_threshold and current_price > inds['ma5'][0]: is_short = False # 避免极度超卖反弹
        if self.p.short_momentum and short_ann > -self.p.short_threshold: is_short = False
        if max(d1, d2, d3) > 1.10: is_short = False # 单日暴涨 > 10%
        if is_high_vol and annualized_returns < -0.5: is_short = False # 暴跌且爆量，可能是恐慌盘见底
        if score >= -self.p.min_score: is_short = False

        if is_short: return score, -1

        return score, 0

    def next(self):
        if len(self) < self.p.lookback_days:
            return

        long_scores = []
        short_scores = []

        # 1. 评分与多空分类
        for d in self.datas:
            score, direction = self.calc_momentum_score(d)
            if direction == 1:
                long_scores.append((score, d))
            elif direction == -1:
                short_scores.append((score, d))
        
        # 做多按得分降序，做空按得分升序（找最负的）
        long_scores.sort(key=lambda x: x[0], reverse=True)
        short_scores.sort(key=lambda x: x[0], reverse=False)

        valid_long_names = [x[1]._name for x in long_scores]
        valid_short_names = [x[1]._name for x in short_scores]

        target_longs = []
        target_shorts = []
        
        current_positions = {d: self.getposition(d).size for d in self.datas if self.getposition(d).size != 0}
        
        # 2. 缓冲池逻辑 (优先保留旧仓位以降低摩擦)
        top_long_buffer = valid_long_names[:self.p.buffer_top_n]
        for d, size in current_positions.items():
            if size > 0 and d._name in top_long_buffer and len(target_longs) < self.p.hold_num:
                target_longs.append(d)
                
        top_short_buffer = valid_short_names[:self.p.buffer_top_n]
        for d, size in current_positions.items():
            if size < 0 and d._name in top_short_buffer and len(target_shorts) < self.p.hold_num:
                target_shorts.append(d)

        # 3. 填补空位
        for score, d in long_scores:
            if len(target_longs) >= self.p.hold_num: break
            if d not in target_longs: target_longs.append(d)
            
        for score, d in short_scores:
            if len(target_shorts) >= self.p.hold_num: break
            if d not in target_shorts: target_shorts.append(d)

        target_names = [d._name for d in target_longs] + [d._name for d in target_shorts]

        # 4. 执行调仓
        # 4.1 卖出/平仓 不在目标列表中的持仓
        for d, size in current_positions.items():
            if d._name not in target_names:
                self.close(d)
                action = "平多" if size > 0 else "平空"
                self.log(f"{action}: {d._name}")

        # 4.2 计算资金分配比例 (对冲配置：一半多，一半空)
        total_slots = self.p.hold_num * 2 if self.p.allow_short else self.p.hold_num
        target_weight = 1.0 / total_slots if total_slots > 0 else 0

        # 4.3 建仓/调仓
        for d in target_longs:
            self.order_target_percent(d, target=target_weight)
            self.log(f"目标做多: {d._name}, 比例: {target_weight*100:.1f}%")
            
        for d in target_shorts:
            # target 为负数，Backtrader 自动识别为做空逻辑
            self.order_target_percent(d, target=-target_weight)
            self.log(f"目标做空: {d._name}, 比例: {-target_weight*100:.1f}%")

    def log(self, txt, dt=None):
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