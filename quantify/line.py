import backtrader as bt
import pandas as pd
import datetime
import sys
import os

class TestStrategy(bt.Strategy):
    def __init__(self):
        self.data = self.datas[0]
        self.sma = bt.indicators.MovingAverageSimple(self.data.close, period=15)
        self.rsi = bt.indicators.RSI(self.data.close)

    def next(self):
        if self.data.close[0] > self.sma[0] and self.data.close[-1] < self.sma[-1]:
            self.buy()
        if self.rsi[0] > 70:
            self.sell()
    