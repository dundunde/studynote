import pandas as pd
import matplotlib.pyplot as plt
import requests
import io

print("正在通过 requests 伪装浏览器拉取 FRED 数据，请稍候...")

# 1. 设置请求头，伪装成正常的 Chrome 浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

# 2. 编写一个带容错的数据拉取函数
def fetch_fred_data(series_id):
    url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}'
    
    # 如果您在本地开启了代理工具（如Clash/V2ray），且Python未自动识别，
    # 可以取消下面这行代理设置的注释，并将端口改为您自己的本地代理端口：
    # proxies = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
    # response = requests.get(url, headers=headers, proxies=proxies)
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"请求失败，状态码: {response.status_code}")
        
    # 检查返回的内容是否是真正的CSV (第一行应该包含 DATE)
    if "DATE" not in response.text[:20]:
        raise Exception(f"被防火墙拦截，返回了非CSV内容:\n{response.text[:200]}")
        
    # 使用 io.StringIO 将文本流转换为 pandas 可读的格式
    return pd.read_csv(io.StringIO(response.text), index_col='DATE', parse_dates=True, na_values='.')

# 3. 拉取数据并处理异常
try:
    sp500 = fetch_fred_data('SP500')
    vix = fetch_fred_data('VIXCLS')
except Exception as e:
    print(f"\n数据拉取中断: {e}")
    exit()

# 4. 数据合并与截取
data = pd.concat([sp500['SP500'], vix['VIXCLS']], axis=1)
data = data.dropna()
data = data.last("2Y") # 取最近两年数据

# 5. 绘图部分 (与之前一致)
fig, ax1 = plt.subplots(figsize=(14, 7))

color_sp = '#1f77b4'
ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('S&P 500', color=color_sp, fontsize=12)
line1 = ax1.plot(data.index, data['SP500'], color=color_sp, label='S&P 500', linewidth=2)
ax1.tick_params(axis='y', labelcolor=color_sp)

ax2 = ax1.twinx()
color_vix = '#d62728'
ax2.set_ylabel('VIX', color=color_vix, fontsize=12)
line2 = ax2.plot(data.index, data['VIXCLS'], color=color_vix, label='VIX', linewidth=1.5, alpha=0.7)
ax2.tick_params(axis='y', labelcolor=color_vix)

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', fontsize=12)

plt.title('S&P 500 vs VIX Trend', fontsize=16, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.6)

fig.tight_layout()
plt.show()