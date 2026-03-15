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

class CryptoRsrsMacdStrategy(bt.Strategy):
    """
    加密货币 RSRS + MACD背离 + ATR移动止损 策略
    """
    params = dict(
        # 止盈止损参数
        atr_period=14,
        atr_mult=2.5,
        profit_target=2.0,        # 翻倍止盈 (价格 >= 成本 * 2)
        time_sl_bars=30,          # 时间止损K线数 (对应原策略30天)
        time_sl_profit=0.05,      # 时间止损最低收益率要求
        
        # MACD择时参数
        macd_fast=12,
        macd_slow=26,
        macd_signal=9,
        macd_window=10,           # 背离检测窗口
        
        # RSRS参数
        rsrs_n=18,                # 回归周期
        rsrs_m=600,               # 标准化周期 (注意：策略需要至少600根K线预热)
        rsrs_buy_threshold=0.7,   # RSRS买入阈值
        rsrs_sell_threshold=-0.7, # RSRS卖出阈值
        rsrs_extreme_weak=-1.5    # RSRS极弱平仓阈值
    )

    def __init__(self):
        # 初始化内置指标
        self.macd = bt.indicators.MACD(
            self.data.close,
            period_me1=self.p.macd_fast,
            period_me2=self.p.macd_slow,
            period_signal=self.p.macd_signal
        )
        self.atr = bt.indicators.ATR(self.data, period=self.p.atr_period)

        # 状态记录变量
        self.stop_price = None
        self.entry_bar = None
        self.rsrs_slopes = deque(maxlen=self.p.rsrs_m)
        self.order = None

    def calc_rsrs(self):
        """计算 RSRS 标准分"""
        if len(self) < self.p.rsrs_n:
            return 0.0

        # 获取过去 N 根 K 线的最高价和最低价
        highs = np.array(self.data.high.get(size=self.p.rsrs_n))
        lows = np.array(self.data.low.get(size=self.p.rsrs_n))

        if len(highs) == self.p.rsrs_n:
            # 线性回归: high = beta * low + alpha
            beta = np.polyfit(lows, highs, 1)[0]
            
            # 计算相关系数 R
            corr_matrix = np.corrcoef(highs, lows)
            if corr_matrix.shape == (2, 2):
                r_squared = corr_matrix[0, 1] ** 2
            else:
                r_squared = 0
                
            # R² 加权修正
            weighted_slope = beta * r_squared
            self.rsrs_slopes.append(weighted_slope)

        if len(self.rsrs_slopes) < self.p.rsrs_m:
            return 0.0

        # 标准化处理 (Z-Score)
        slopes_arr = np.array(self.rsrs_slopes)
        mean_slope = np.mean(slopes_arr)
        std_slope = np.std(slopes_arr)

        if std_slope < 1e-6:
            return 0.0

        return (self.rsrs_slopes[-1] - mean_slope) / std_slope

    def check_macd_divergence(self):
        """检测 MACD 顶背离 (价格上涨，MACD下跌)"""
        if len(self) < self.p.macd_window:
            return False

        prices = np.array(self.data.close.get(size=self.p.macd_window))
        difs = np.array(self.macd.macd.get(size=self.p.macd_window))
        x = np.arange(self.p.macd_window)

        if len(prices) == self.p.macd_window:
            slope_price = np.polyfit(x, prices, 1)[0]
            slope_dif = np.polyfit(x, difs, 1)[0]

            # 顶背离：价格呈上升趋势，但 DIF 呈下降趋势
            if slope_price > 0.01 and slope_dif < -0.001:
                # 确认 MACD 柱子/DIF 是否在走弱
                if self.macd.macd[0] < self.macd.macd[-1]:
                    return True  # 触发风险信号
        return False

    def notify_order(self, order):
        """订单状态监控"""
        if order.status in [order.Submitted, order.Accepted]:
            return
        self.order = None  # 订单执行完毕重置状态

    def next(self):
        # 避免在有挂单时重复下单
        if self.order:
            return

        # 1. 计算核心指标
        rsrs_score = self.calc_rsrs()
        macd_risk = self.check_macd_divergence()

        # 2. 开仓逻辑
        if not self.position:
            # 市场无顶背离风险，且 RSRS 处于强势区间
            if not macd_risk and rsrs_score > self.p.rsrs_buy_threshold:
                # 为了简便，这里直接满仓买入。可以根据需要替换为按比例买入 (如 setposition)
                self.order = self.buy()
                # 记录开仓信息
                self.entry_bar = len(self)
                # 初始化 ATR 止损位
                self.stop_price = self.data.close[0] - self.p.atr_mult * self.atr[0]
                self.log(f'BUY EXECUTED, Price: {self.data.close[0]:.2f}, Init Stop: {self.stop_price:.2f}')

        # 3. 持仓维护与平仓逻辑
        else:
            current_price = self.data.close[0]
            entry_price = self.position.price
            
            # -- ATR 移动止损 (只涨不跌) --
            new_stop = current_price - self.p.atr_mult * self.atr[0]
            if new_stop > self.stop_price:
                self.stop_price = new_stop

            # 触发条件 1: 大盘极弱防御清仓 (RSRS < -1.5)
            if rsrs_score < self.p.rsrs_extreme_weak:
                self.log(f'RSRS EXTREME WEAK EXIT: {rsrs_score:.2f}')
                self.order = self.close()
                return

            # 触发条件 2: 翻倍止盈
            if current_price >= entry_price * self.p.profit_target:
                self.log(f'TAKE PROFIT EXIT, Price: {current_price:.2f}')
                self.order = self.close()
                return

            # 触发条件 3: ATR 移动止损
            if current_price <= self.stop_price:
                self.log(f'ATR STOP LOSS EXIT, Price: {current_price:.2f}, Stop: {self.stop_price:.2f}')
                self.order = self.close()
                return

            # 触发条件 4: 时间止损
            held_bars = len(self) - self.entry_bar
            if held_bars >= self.p.time_sl_bars:
                profit_rate = (current_price / entry_price) - 1
                if profit_rate < self.p.time_sl_profit:
                    self.log(f'TIME STOP EXIT, Held Bars: {held_bars}, Profit: {profit_rate*100:.2f}%')
                    self.order = self.close()
                    return

    def log(self, txt, dt=None):
        """简易日志输出"""
        dt = dt or self.data.datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

if __name__ == '__main__':
    # 创建对象并添加策略
    cerebro = bt.Cerebro()
    # 可以在添加策略时修改参数的默认值
    cerebro.addstrategy(CryptoRsrsMacdStrategy)
    # cerebro.optstrategy(
    #     TestStrategy,
    #     maperiod=range(10,31),
    # )

    # 加载数据
    start_date = '2023-01-01'
    end_date = '2026-01-01'
    data = pd.read_csv(
        "./quantify/data/BTCUSDT_4h_2020_2026_Clean.csv",
        index_col='datetime',
        parse_dates=['datetime']
        )
    data = data.loc[start_date:end_date]
    # data = data[:-2000]
    # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # datapath = os.path.join(modpath, './data/orcl-1995-2014.txt')
    # data = data.iloc[-1000:]
    data_1 = bt.feeds.PandasData(
        dataname=data,
        datetime=None,  # None 表示直接使用 DataFrame 的索引 (即我们刚刚转换好的 DatetimeIndex)
        name='BTCUSDT',
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume',
        openinterest=-1 # 如果你的数据里没有持仓量列，设为 -1 表示忽略
    )

    data_2 = bt.feeds.PandasData(
        dataname=data,
        datetime=None,  # None 表示直接使用 DataFrame 的索引 (即我们刚刚转换好的 DatetimeIndex)
        name='BTCUSDT',
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume',
        openinterest=-1 # 如果你的数据里没有持仓量列，设为 -1 表示忽略
    )

    cerebro.adddata(data=data_1)
    # cerebro.adddata(data=data_2)

    # 设置金额和佣金
    cerebro.broker.setcash(2000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=0.01)  # 每次买入 0.01 个 BTC
    cerebro.broker.setcommission(commission=0.001)

    # 4. 添加 TimeReturn 分析器，用来记录每日收益率
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')

    print('初始投资组合价值：%.2f' % cerebro.broker.getvalue())
    
    # 5. 运行回测并接收返回结果
    results = cerebro.run(maxcpus=1)
    strat = results[0] # 获取第一个策略实例
    print('最终投资组合价值：%.2f' % cerebro.broker.getvalue())

    # cerebro.plot(style='candlestick')

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
