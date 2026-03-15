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
    加密货币 RSRS + MACD背离 + ATR移动止损 策略 (支持多空双向，多空参数独立)
    """
    params = dict(
        # --- 独立的多空止盈止损参数 ---
        atr_period=14,
        
        long_atr_mult=2.5,        # 多头 ATR 止损乘数
        short_atr_mult=1.5,       # 空头 ATR 止损乘数 (通常空头需要更紧的止损)
        
        long_profit_target=2.0,   # 多头止盈目标 (2.0 = 100% 收益率)
        short_profit_target=1.5,  # 空头止盈目标 (1.5 = 50% 收益率，空单翻倍极难)
        
        time_sl_bars=30,          # 时间止损K线数
        time_sl_profit=0.05,      # 时间止损最低收益率要求
        
        # --- MACD择时参数 ---
        macd_fast=12,
        macd_slow=26,
        macd_signal=9,
        macd_window=10,           # 背离检测窗口
        
        # --- RSRS参数 ---
        rsrs_n=18,                # 回归周期
        rsrs_m=600,               # 标准化周期
        rsrs_buy_threshold=0.7,   # RSRS做多买入阈值
        rsrs_sell_threshold=-0.7, # RSRS做空卖出阈值
        rsrs_extreme_weak=-1.5,   # RSRS极弱平多仓阈值
        rsrs_extreme_strong=1.5   # RSRS极强平空仓阈值
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

        highs = np.array(self.data.high.get(size=self.p.rsrs_n))
        lows = np.array(self.data.low.get(size=self.p.rsrs_n))

        if len(highs) == self.p.rsrs_n:
            beta = np.polyfit(lows, highs, 1)[0]
            corr_matrix = np.corrcoef(highs, lows)
            if corr_matrix.shape == (2, 2):
                r_squared = corr_matrix[0, 1] ** 2
            else:
                r_squared = 0
                
            weighted_slope = beta * r_squared
            self.rsrs_slopes.append(weighted_slope)

        if len(self.rsrs_slopes) < self.p.rsrs_m:
            return 0.0

        slopes_arr = np.array(self.rsrs_slopes)
        mean_slope = np.mean(slopes_arr)
        std_slope = np.std(slopes_arr)

        if std_slope < 1e-6:
            return 0.0

        return (self.rsrs_slopes[-1] - mean_slope) / std_slope

    def check_macd_divergences(self):
        """检测 MACD 顶背离和底背离"""
        top_div = False
        bot_div = False
        
        if len(self) < self.p.macd_window:
            return top_div, bot_div

        prices = np.array(self.data.close.get(size=self.p.macd_window))
        difs = np.array(self.macd.macd.get(size=self.p.macd_window))
        x = np.arange(self.p.macd_window)

        if len(prices) == self.p.macd_window:
            slope_price = np.polyfit(x, prices, 1)[0]
            slope_dif = np.polyfit(x, difs, 1)[0]

            # 顶背离：价格呈上升趋势，但 DIF 呈下降趋势且走弱
            if slope_price > 0.01 and slope_dif < -0.001:
                if self.macd.macd[0] < self.macd.macd[-1]:
                    top_div = True
                    
            # 底背离：价格呈下降趋势，但 DIF 呈上升趋势且走强
            if slope_price < -0.01 and slope_dif > 0.001:
                if self.macd.macd[0] > self.macd.macd[-1]:
                    bot_div = True
                    
        return top_div, bot_div

    def notify_order(self, order):
        """订单状态监控"""
        if order.status in [order.Submitted, order.Accepted]:
            return
        self.order = None

    def next(self):
        if self.order:
            return

        # 1. 计算核心指标
        rsrs_score = self.calc_rsrs()
        top_risk, bot_risk = self.check_macd_divergences()

        # 2. 开仓逻辑
        if not self.position:
            # 【做多条件】：无顶背离，RSRS 强势
            if not top_risk and rsrs_score > self.p.rsrs_buy_threshold:
                self.order = self.buy()
                self.entry_bar = len(self)
                # 使用多头 ATR 参数计算初始止损
                self.stop_price = self.data.close[0] - self.p.long_atr_mult * self.atr[0]
                self.log(f'LONG ENTRY EXECUTED, Price: {self.data.close[0]:.2f}, Init Stop: {self.stop_price:.2f}')
                
            # 【做空条件】：无底背离，RSRS 弱势
            elif not bot_risk and rsrs_score < self.p.rsrs_sell_threshold:
                self.order = self.sell()
                self.entry_bar = len(self)
                # 使用空头 ATR 参数计算初始止损
                self.stop_price = self.data.close[0] + self.p.short_atr_mult * self.atr[0]
                self.log(f'SHORT ENTRY EXECUTED, Price: {self.data.close[0]:.2f}, Init Stop: {self.stop_price:.2f}')

        # 3. 持仓维护与平仓逻辑
        else:
            current_price = self.data.close[0]
            entry_price = self.position.price
            held_bars = len(self) - self.entry_bar

            # --- 多头持仓逻辑 ---
            if self.position.size > 0:
                profit_rate = (current_price - entry_price) / entry_price
                target_profit_rate = self.p.long_profit_target - 1.0 # 获取多头目标利润率
                
                # 多头 ATR 移动止损 (只涨不跌)
                new_stop = current_price - self.p.long_atr_mult * self.atr[0]
                if new_stop > self.stop_price:
                    self.stop_price = new_stop

                # 触发条件 1: 大盘极弱防御清仓 (RSRS < -1.5)
                if rsrs_score < self.p.rsrs_extreme_weak:
                    self.log(f'LONG RSRS EXTREME WEAK EXIT: {rsrs_score:.2f}')
                    self.order = self.close()
                # 触发条件 2: 目标止盈
                elif profit_rate >= target_profit_rate:
                    self.log(f'LONG TAKE PROFIT EXIT, Price: {current_price:.2f}, Profit: {profit_rate*100:.2f}%')
                    self.order = self.close()
                # 触发条件 3: ATR 移动止损
                elif current_price <= self.stop_price:
                    self.log(f'LONG ATR STOP EXIT, Price: {current_price:.2f}, Stop: {self.stop_price:.2f}')
                    self.order = self.close()
                # 触发条件 4: 时间止损
                elif held_bars >= self.p.time_sl_bars and profit_rate < self.p.time_sl_profit:
                    self.log(f'LONG TIME STOP EXIT, Held Bars: {held_bars}, Profit: {profit_rate*100:.2f}%')
                    self.order = self.close()

            # --- 空头持仓逻辑 ---
            elif self.position.size < 0:
                profit_rate = (entry_price - current_price) / entry_price
                target_profit_rate = self.p.short_profit_target - 1.0 # 获取空头目标利润率
                
                # 空头 ATR 移动止损 (只跌不涨)
                new_stop = current_price + self.p.short_atr_mult * self.atr[0]
                if new_stop < self.stop_price:
                    self.stop_price = new_stop

                # 触发条件 1: 大盘极强防御清仓 (RSRS > 1.5)
                if rsrs_score > self.p.rsrs_extreme_strong:
                    self.log(f'SHORT RSRS EXTREME STRONG EXIT: {rsrs_score:.2f}')
                    self.order = self.close()
                # 触发条件 2: 目标止盈
                elif profit_rate >= target_profit_rate:
                    self.log(f'SHORT TAKE PROFIT EXIT, Price: {current_price:.2f}, Profit: {profit_rate*100:.2f}%')
                    self.order = self.close()
                # 触发条件 3: ATR 移动止损被触发
                elif current_price >= self.stop_price:
                    self.log(f'SHORT ATR STOP EXIT, Price: {current_price:.2f}, Stop: {self.stop_price:.2f}')
                    self.order = self.close()
                # 触发条件 4: 时间止损
                elif held_bars >= self.p.time_sl_bars and profit_rate < self.p.time_sl_profit:
                    self.log(f'SHORT TIME STOP EXIT, Held Bars: {held_bars}, Profit: {profit_rate*100:.2f}%')
                    self.order = self.close()

    def log(self, txt, dt=None):
        """简易日志输出"""
        dt = dt or self.data.datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(CryptoRsrsMacdStrategy)

    start_date = '2023-01-01'
    end_date = '2026-01-01'
    data = pd.read_csv(
        "./quantify/data/BTCUSDT_4h_2020_2026_Clean.csv",
        index_col='datetime',
        parse_dates=['datetime']
        )
    data = data.loc[start_date:end_date]
    
    data_1 = bt.feeds.PandasData(
        dataname=data,
        datetime=None,
        name='BTCUSDT',
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume',
        openinterest=-1
    )

    cerebro.adddata(data=data_1)
    
    cerebro.broker.setcash(2000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=0.01)
    cerebro.broker.setcommission(commission=0.001)

    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')

    print('初始投资组合价值：%.2f' % cerebro.broker.getvalue())
    results = cerebro.run(maxcpus=1)
    strat = results[0]
    print('最终投资组合价值：%.2f' % cerebro.broker.getvalue())

    b = Bokeh(style='bar', plot_mode='single', scheme=Tradimo(), use_cdn=False)
    cerebro.plot(b)

    portfolio_stats = strat.analyzers.getbyname('_TimeReturn')
    returns = portfolio_stats.get_analysis()

    returns_series = pd.Series(returns)
    returns_series.index = pd.to_datetime(returns_series.index)
    returns_series.index = returns_series.index.tz_localize(None)

    print("正在生成 QuantStats 报告...")
    qs.reports.html(returns_series, output='strategy_report.html', title='Crypto RSRS MACD 多空策略回测')
    print("报告生成完毕！请在文件夹中双击打开 strategy_report.html")