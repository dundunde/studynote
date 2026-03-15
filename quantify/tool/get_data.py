import os
import requests
import hashlib
from datetime import datetime
import pandas as pd

# ================= 配置参数 =================
SYMBOL = "BTCUSDT"      # 交易对名称
INTERVAL = "1d"        # K线级别
START_DATE = "2020-01-01"
# 自动获取当前月份作为结束时间
END_DATE = datetime.now().strftime("%Y-%m-%d") 

# Binance 官方 U本位合约 数据接口前缀
BASE_URL = f"https://data.binance.vision/data/futures/um/monthly/klines/{SYMBOL}/{INTERVAL}/"
# 本地保存目录
DOWNLOAD_DIR = f"./binance_data/{SYMBOL}_{INTERVAL}"

# 创建存储目录
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
# ============================================

def calculate_sha256(filepath):
    """计算文件的 SHA256 哈希值"""
    sha256_hash = hashlib.sha256()
    # 分块读取，避免大文件占用过多内存
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_and_verify(date_str):
    """下载对应月份的 zip 和 checksum 并进行比对"""
    zip_filename = f"{SYMBOL}-{INTERVAL}-{date_str}.zip"
    checksum_filename = f"{zip_filename}.CHECKSUM"

    zip_url = BASE_URL + zip_filename
    checksum_url = BASE_URL + checksum_filename

    zip_path = os.path.join(DOWNLOAD_DIR, zip_filename)
    checksum_path = os.path.join(DOWNLOAD_DIR, checksum_filename)

    print(f"开始处理 {date_str} 数据...")

    # 1. 下载 CHECKSUM 文件
    response_chk = requests.get(checksum_url)
    if response_chk.status_code != 200:
        print(f"  [-] 找不到 {date_str} 的校验文件，可能该月尚未生成数据。")
        return

    with open(checksum_path, 'wb') as f:
        f.write(response_chk.content)

    # 读取官方哈希值 (CHECKSUM 文件内的格式通常为: hash_value  filename)
    with open(checksum_path, 'r') as f:
        official_hash = f.read().split()[0]

    # 2. 检查本地是否已有完好的 zip 文件，实现断点续传/跳过已下载逻辑
    if os.path.exists(zip_path):
        local_hash = calculate_sha256(zip_path)
        if local_hash == official_hash:
            print(f"  [+] 本地文件已存在且校验通过，跳过下载。")
            return
        else:
            print(f"  [*] 本地文件已损坏或不完整，准备重新下载...")

    # 3. 下载 ZIP 文件
    print(f"  [*] 正在下载 {zip_filename} ...")
    response_zip = requests.get(zip_url, stream=True)
    if response_zip.status_code == 200:
        with open(zip_path, 'wb') as f:
            for chunk in response_zip.iter_content(chunk_size=8192):
                f.write(chunk)

        # 4. 下载完成后再次校验
        new_local_hash = calculate_sha256(zip_path)
        if new_local_hash == official_hash:
            print(f"  [+] {zip_filename} 下载并校验成功！")
        else:
            print(f"  [-] {zip_filename} 校验失败，文件可能在下载时损坏，已将其删除。")
            os.remove(zip_path)
    else:
        print(f"  [-] 下载 ZIP 失败，HTTP 状态码: {response_zip.status_code}")

# ================= 主程序执行 =================
if __name__ == "__main__":
    # 使用 pandas 生成从开始日期到现在的月份列表 (格式: YYYY-MM)
    # 'MS' 表示 Month Start
    months = pd.date_range(start=START_DATE, end=END_DATE, freq='MS').strftime("%Y-%m").tolist()

    print(f"计划获取 {SYMBOL} {INTERVAL} 级别从 {months[0]} 到 {months[-1]} 的数据...\n")
    
    for month in months:
        download_and_verify(month)

    print("\n全部任务执行完毕！")