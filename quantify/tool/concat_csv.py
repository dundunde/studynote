import pandas as pd
import glob
import os

# ================= 配置参数 =================
SYMBOL = "BTCUSDT"      # 交易对名称
INTERVAL = "1d"        # K线级别

def load_and_concat_mixed_binance_data(folder_path):
    """
    自适应读取含有/不含有表头的币安历史数据，并完美拼接
    """
    search_pattern = os.path.join(folder_path, f"{SYMBOL}-{INTERVAL}-*.csv")
    print(f"路径:{search_pattern}")
    all_files = glob.glob(search_pattern)
    
    if not all_files:
        print("未找到任何 CSV 文件，请检查路径！")
        return None
        
    print(f"共找到 {len(all_files)} 个 CSV 文件，开始自适应读取...")

    # 我们统一使用的规范列名 (对应币安标准的 12 列)
    columns = [
        'open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ]

    df_list = []
    
    for file in all_files:
        # 1. “偷看”第一行：判断是否有表头
        with open(file, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            
        # 2. 如果第一行的第一个字符不是数字 (比如是字母 'o')，说明存在表头
        has_header = not first_line[0].isdigit()
        
        # 3. 自适应加载：有表头则用 header=0 替换为我们自定义的列名，无表头则用 header=None
        if has_header:
            df = pd.read_csv(file, names=columns, header=0)
        else:
            df = pd.read_csv(file, names=columns, header=None)
            
        df_list.append(df)

    print("读取完成，正在合并与格式化...")
    # 把所有的 DataFrame 竖向拼接到一起
    full_df = pd.concat(df_list, ignore_index=True)

    # ==========================================
    # 数据清洗与格式化
    # ==========================================
    
    # 将开盘时间戳转换为带时区 (东八区) 的 datetime
    # (如果原数据里的数字带有引号变成了字符串，强制转为 float 即可)
    full_df['open_time'] = full_df['open_time'].astype(float)
    full_df['datetime'] = pd.to_datetime(full_df['open_time'], unit='ms') + pd.Timedelta(hours=8)
    
    # 提取核心 K 线列，并将所有的价格转为浮点数，以防混入字符串
    core_columns = ['open', 'high', 'low', 'close', 'volume']
    full_df[core_columns] = full_df[core_columns].astype(float)
    
    # 提取需要的列并设置索引
    full_df = full_df[['datetime'] + core_columns]
    full_df.set_index('datetime', inplace=True)
    
    # 按时间从早到晚排序 (极其重要)
    full_df.sort_index(inplace=True)
    
    # 去重处理
    full_df = full_df[~full_df.index.duplicated(keep='first')]
    
    return full_df

# ================= 实际执行 =================
if __name__ == '__main__':
    # 替换为你存放 CSV 文件的真实文件夹路径
    folder_path = f'./binance_data/{SYMBOL}_{INTERVAL}/csv_files' 
    
    df_history = load_and_concat_mixed_binance_data(folder_path)
    
    if df_history is not None:
        print("\n=== 数据处理成功 ===")
        print(df_history.head(3))
        print("...")
        print(df_history.tail(3))
        
        print(f"\n跨度: {df_history.index.min()} 到 {df_history.index.max()}")
        print(f"K线数量: {len(df_history)} 根")
        
        # 保存为一个完美的新文件，供回测引擎使用
        save_name = f'{SYMBOL}_{INTERVAL}_2020_2026_Clean.csv'
        df_history.to_csv(save_name)
        print(f"\n完美合并！请在 Backtrader 中直接加载: {save_name}")