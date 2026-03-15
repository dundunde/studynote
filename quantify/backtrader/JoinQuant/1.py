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


class FinalValueAnalyzer(bt.Analyzer):
    def start(self):
        # 初始化一个变量
        self.final_val = 0.0

    def stop(self):
        # 回测刚结束、策略对象还没被销毁时触发
        # 此时 self.strategy 健在，赶紧把资金记下来
        self.final_val = self.strategy.broker.getvalue()

    def get_analysis(self):
        # 当外部提取分析结果时，直接交出我们存好的数值
        return {"final_value": self.final_val}


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

    # 1. 使用 optstrategy 进行参数寻优
    # 这里我们对 多/空 的 ATR乘数 和 止盈目标 进行组合测试
    # 注意：传给优化的参数必须是可迭代对象 (比如 tuple, list, 或者 range)
    cerebro.optstrategy(
        CryptoRsrsMacdStrategy,
        long_atr_mult=(2.0, 2.5, 3.0),         # 测试 3 个值
        long_profit_target=(1.5, 2.0),         # 测试 2 个值
        short_atr_mult=(1.0, 1.5, 2.0),        # 测试 3 个值
        short_profit_target=(1.2, 1.5)         # 测试 2 个值
        # 组合总数 = 3 * 2 * 3 * 2 = 36 种情况
    )

    # 2. 加载数据
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
    
    # 3. 设置初始资金和手续费
    cerebro.broker.setcash(2000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=0.01)
    cerebro.broker.setcommission(commission=0.001)

    # 添加分析器来评估每个组合的收益和回撤
    cerebro.addanalyzer(bt.analyzers.Returns, _name='_Returns')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')
    
    # --- 新增：把我们的自定义分析器加进去 ---
    cerebro.addanalyzer(FinalValueAnalyzer, _name='_FinalValue')
    print('开始并行参数优化，请耐心等待...')
    
    # 4. 运行回测 (maxcpus=None 表示使用全部 CPU 核心)
    # 优化模式下，这里返回的是一个由列表组成的列表
    results = cerebro.run(maxcpus=None) 

    # 5. 解析并收集所有参数组合的回测结果
    final_results_list = []
    
    for run in results:
        for strat in run:
            p = strat.params
            
            # --- 修改：从我们自定义的分析器中提取最终资金 ---
            final_value_dict = strat.analyzers.getbyname('_FinalValue').get_analysis()
            final_value = final_value_dict.get('final_value', 2000.0)
            
            # 获取分析器的数据 (比如总收益率和最大回撤)
            ret_analyzer = strat.analyzers.getbyname('_Returns').get_analysis()
            dd_analyzer = strat.analyzers.getbyname('_DrawDown').get_analysis()
            
            # 收益率，如果全是亏损可能获取不到，做一下容错处理
            total_return = ret_analyzer.get('rtot', 0) * 100 
            max_drawdown = dd_analyzer.get('max', {}).get('drawdown', 0)

            final_results_list.append({
                '多头ATR': p.long_atr_mult,
                '多头止盈': p.long_profit_target,
                '空头ATR': p.short_atr_mult,
                '空头止盈': p.short_profit_target,
                '最终资金': round(final_value, 2),
                '总收益率(%)': round(total_return, 2),
                '最大回撤(%)': round(max_drawdown, 2)
            })

    # 6. 使用 Pandas 对结果进行排序并输出
    df_results = pd.DataFrame(final_results_list)
    
    # 按照 "最终资金" 从高到低排序
    df_results = df_results.sort_values(by='最终资金', ascending=False)
    
    print("\n" + "="*50)
    print("参数优化完成！排名前 10 的参数组合如下：")
    print("="*50)
    print(df_results.head(10).to_string(index=False))
    
    # 可选：将所有结果保存到 CSV 慢慢分析
    df_results.to_csv("optimization_results.csv", index=False)
    print("\n完整优化结果已保存到 optimization_results.csv")