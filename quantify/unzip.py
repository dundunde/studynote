import os
import zipfile

# ================= 配置参数 =================
SYMBOL = "BTCUSDT"      # 交易对名称
INTERVAL = "2h"        # K线级别
# 这里的路径需要与你上一个下载脚本的路径保持一致
DOWNLOAD_DIR = f"./binance_data/{SYMBOL}_{INTERVAL}"

# 提取后的 CSV 文件存放路径
EXTRACT_DIR = os.path.join(DOWNLOAD_DIR, "csv_files")

# 设置为 True 可以在解压成功后自动删除原来的 .zip 文件以节省硬盘空间
DELETE_ZIP_AFTER_EXTRACT = False
# ============================================

def extract_all_zips():
    # 检查下载目录是否存在
    if not os.path.exists(DOWNLOAD_DIR):
        print(f"[-] 错误：找不到目录 {DOWNLOAD_DIR}。请确认下载脚本已成功运行。")
        return

    # 创建存放解压后 CSV 文件的目录
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    # 获取目录下所有的 .zip 文件
    files = os.listdir(DOWNLOAD_DIR)
    zip_files = [f for f in files if f.endswith('.zip')]

    if not zip_files:
        print(f"[-] 在 {DOWNLOAD_DIR} 中没有找到任何 .zip 文件。")
        return

    print(f"[*] 找到 {len(zip_files)} 个 .zip 文件，开始解压至 {EXTRACT_DIR} ...\n")

    success_count = 0
    fail_count = 0

    for zip_filename in sorted(zip_files):
        zip_filepath = os.path.join(DOWNLOAD_DIR, zip_filename)

        try:
            # 尝试打开并解压 zip 文件
            with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                # 币安的压缩包通常里面只有一个同名的 .csv 文件
                extracted_files = zip_ref.namelist()
                # 解压到指定目录
                zip_ref.extractall(EXTRACT_DIR)
                print(f"  [+] 成功解压: {zip_filename} -> 包含 {len(extracted_files)} 个文件")
                success_count += 1

            # 如果配置了删除原文件且解压成功
            if DELETE_ZIP_AFTER_EXTRACT:
                os.remove(zip_filepath)
                print(f"      清理: 已删除原压缩包 {zip_filename}")

        except zipfile.BadZipFile:
            print(f"  [x] 解压失败，文件损坏或不是有效的 zip 格式: {zip_filename}")
            fail_count += 1
        except Exception as e:
            print(f"  [x] 处理 {zip_filename} 时发生未知错误: {e}")
            fail_count += 1

    print("\n================ 执行报告 ================")
    print(f"总计找到压缩包: {len(zip_files)} 个")
    print(f"成功解压: {success_count} 个")
    print(f"解压失败: {fail_count} 个")
    print(f"解压后的文件保存在: {os.path.abspath(EXTRACT_DIR)}")

if __name__ == "__main__":
    extract_all_zips()