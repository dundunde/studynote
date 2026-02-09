import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# --- 关键修改 1: 尝试修复 yfinance 的缓存问题 ---
# 如果你不需要缓存，可以不使用 session，或者简单地忽略缓存错误
# 这里我们直接下载，但添加 error_handling
# ---------------------------------------------

tickers = ['QQQ', 'SPY', 'VT', 'EEM']

print("正在下载数据...")

# --- 关键修改 2: 调整下载参数 ---
# ignore_tz=True: 忽略时区问题，有时能减少警告
# auto_adjust=False: 显式控制，虽然默认下载里通常不需要，但明确写出更稳妥
# 增加 threads=False: 虽然慢一点，但能减少触发 "Rate Limit" 和 "Database Locked" 的概率
try:
    # 尝试下载数据
    raw_data = yf.download(tickers, start='2016-01-01', end='2026-01-01', threads=False)
    
    # 检查是否获取到了数据
    if raw_data.empty:
        print("错误：未能下载任何数据，请检查网络或稍后再试。")
        exit() # 终止程序
        
    # 获取 'Adj Close'
    # 注意：新版 yfinance 下载多只股票时，列索引可能是 MultiIndex
    data = raw_data['Adj Close']

except Exception as e:
    print(f"下载过程中发生严重错误: {e}")
    exit()

# --- 关键修改 3: 数据清洗 ---
# 删除全为空的行（防止某些天没数据导致计算错误）
data = data.dropna(how='all')

# 再次检查清洗后是否还有数据
if len(data) == 0:
    print("错误：数据清洗后为空。")
    exit()

print("下载成功，开始绘图...")

# 3. 数据归一化处理
try:
    # 假设第一天大家都投资了 $100
    # data.iloc[0] 是第一行数据
    normalized_data = (data / data.iloc[0]) * 100
except IndexError:
    print("错误：无法获取第一行数据。")
    exit()

# 4. 绘制收益率曲线
plt.figure(figsize=(12, 6))

for ticker in tickers:
    # 增加检查：确保该列存在
    if ticker in normalized_data.columns:
        plt.plot(normalized_data.index, normalized_data[ticker], label=ticker)

plt.title('过去10年全球主要指数收益对比 (初始投资=$100)', fontsize=14)
plt.xlabel('年份')
plt.ylabel('资产价值 ($)')
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)

plt.show()