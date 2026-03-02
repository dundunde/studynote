import warnings
import matplotlib.dates as mdates
# 【补丁】修复 Backtrader 兼容高版本 matplotlib 的 bug
mdates.warnings = warnings 

import backtrader as bt
import pandas as pd
import ccxt

if __name__ == '__main__':

    cerebro = bt.Cerebro()

    # 现金与手续费
    cerebro.broker.setcash(1000.0)
    cerebro.broker.setcommission(commission=0.003)

    # 获取数据
    try:
        exchange = ccxt.binance({
                'proxies': {
                'http': 'http://127.0.0.1:7897', 
                'https': 'http://127.0.0.1:7897',
            }
            })
        ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='1d', limit=1000)

        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', drop=True, inplace=True)
        
        if df.empty:
            print("警告：未能下载到数据，请检查网络代理（如果在中国大陆，通常需要全局代理）或稍等片刻再试。")
        else:
            print("数据获取成功，开始回测...")
            data = bt.feeds.PandasData(dataname=df)
            cerebro.adddata(data)

            cerebro.run()
            
            print("回测完成，正在生成图表...")
            cerebro.plot(style='bar')

    except Exception as e:
        print(f"执行过程中发生错误: {e}")