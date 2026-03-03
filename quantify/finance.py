"""
1. 使用Bokeh实现网页绘图
2. 使用quantstats
3. ta-lib是什么
"""

# import numpy as np
# # 在所有的 import 之前，强行打个补丁
# if not hasattr(np, 'bool8'):
#     np.bool8 = np.bool_
import os
import sys
import datetime
import pandas as pd
import quantstats as qs
import backtrader as bt

# from backtrader_plotting import Bokeh
# from backtrader_plotting.schemes import Tradimo



class TestStrategy(bt.Strategy):

    params = (
            ('myparam', 27),
            ('exitbars', 5),
            ('maperiod', 5),

            )

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 均线
        self.sma = bt.indicators.MovingAverageSimple(
            self.datas[0],
            period=self.params.maperiod
            )

        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25).subplot = True
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        
    
    def log(self, txt, dt=None, doprint=False):
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order: bt.order.Order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'买入执行,价格：{order.executed.price}'
                    f'成本：{order.executed.value}'
                    f'佣金：{order.executed.comm}'
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.bar_executed = len(self)
            else:
                self.log('卖出执行，价格：%.2f，成本：%.2f，佣金 %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金不足/拒绝')

        self.order = None
    
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        
        self.log(
            f'利润记录，毛利润：{trade.pnl},净利润:{trade.pnlcomm}'
        )
    
    def next(self):
        self.log(f'收盘价:{self.dataclose[0]:.2f}')

        if self.order:
            return
        
        if not self.position:
            # if self.dataclose[0] < self.dataclose[-1]:
            #     if self.dataclose[-1] < self.dataclose[-2]:
            #         self.log('创建买入订单，%.2f' % self.dataclose[0])
            #         self.order = self.buy()

            if self.dataclose[0] > self.sma[0]:
                self.log('创建买入订单，%.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                self.log('创建卖出订单，%.2f' % self.dataclose[0])
                self.order = self.sell()
    
    def stop(self):
        self.log(f'maperiod:{self.params.maperiod} ending value:{self.broker.getvalue():.2f}',doprint=True)



if __name__ == '__main__':
    # 创建对象并添加策略
    cerebro = bt.Cerebro()
    # 可以在添加策略时修改参数的默认值
    # cerebro.addstrategy(TestStrategy,myparam=20, exitbars=7)
    cerebro.optstrategy(
        TestStrategy,
        maperiod=range(10,31),
    )

    # 加载数据
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, './data/orcl-1995-2014.txt')

    data = bt.feeds.YahooFinanceCSVData(
        dataname='c:/Users/dun/Desktop/studynote/studynote/quantify/data/orcl-1995-2014.txt',
        fromdate = datetime.datetime(2000, 1, 1),
        todate = datetime.datetime(2000, 12, 31),
        reverse=False,
        dtformat='%Y-%m-%d',
    )
    cerebro.adddata(data=data)

    # 设置金额和佣金
    cerebro.broker.setcash(1000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.0)

    # 4. 添加 TimeReturn 分析器，用来记录每日收益率
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')

    print('初始投资组合价值：%.2f' % cerebro.broker.getvalue())
    
    # 5. 运行回测并接收返回结果
    results = cerebro.run(maxcpus=1)
    strat = results[0] # 获取第一个策略实例

    # cerebro.plot()
    # b = Bokeh(style='bar', plot_mode='single', scheme=Tradimo())
    # cerebro.plot(b)
    
    # print('最终投资组合价值：%.2f' % cerebro.broker.getvalue())

    # # 6. 提取收益率数据
    # portfolio_stats = strat.analyzers.getbyname('_TimeReturn')
    # returns = portfolio_stats.get_analysis()

    # # 7. 将字典转换为 pandas.Series，并将索引转为日期时间格式
    # # 这一步是必须的，因为 QuantStats 只认 pandas 数据格式
    # returns_series = pd.Series(returns)
    # returns_series.index = pd.to_datetime(returns_series.index)
    
    # # 由于时区问题，需要去掉时区信息（如果有的话），防止 QuantStats 报错
    # returns_series.index = returns_series.index.tz_localize(None)

    # # 8. 使用 QuantStats 生成网页版分析报告
    # # 这会在你脚本的同级目录下生成一个 strategy_report.html 文件
    # print("正在生成 QuantStats 报告...")
    # qs.reports.html(returns_series, output='strategy_report.html', title='Oracle 策略回测报告')
    # print("报告生成完毕！请在文件夹中双击打开 strategy_report.html")
