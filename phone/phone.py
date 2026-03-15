import uiautomator2 as u2
import time
import xml.etree.ElementTree as ET

def export_sogou_clipboard():
    print("正在连接设备...")
    try:
        d = u2.connect() 
        print(f"设备连接成功: {d.info.get('productName', 'Unknown')}")
    except Exception as e:
        print("连接设备失败。")
        return

    print("==================================================")
    print("请打开【微信】聊天框，呼出搜狗【剪贴板】")
    print("==================================================")
    
    for i in range(5, 0, -1):
        print(f"请准备，倒计时 {i} 秒...", end="\r")
        time.sleep(1)
    print("\n开始抓取剪切板内容...\n")

    extracted_texts = []
    seen_texts = set()
    previous_page_content = None
    empty_count = 0

    while True:
        # 【绝杀修改】：不再使用系统查找，而是直接导出屏幕底层 XML 源码
        xml_content = d.dump_hierarchy()
        current_page_content = []

        try:
            # 使用 Python 内置的 XML 解析器，硬核提取数据
            root = ET.fromstring(xml_content)
            # 遍历所有节点，寻找搜狗剪贴板专属 ID
            for node in root.iter('node'):
                if node.get('resource-id') == 'com.sohu.inputmethod.sogou:id/bch':
                    text = node.get('text', '').strip()
                    if text:
                        current_page_content.append(text)
                        
                        if text not in seen_texts:
                            seen_texts.add(text)
                            extracted_texts.append(text)
                            
                            preview = text[:20].replace('\n', ' ').replace('\r', '')
                            print(f"已提取: {preview}...") 
        except Exception as e:
            print(f"解析 XML 时出现小错误: {e}")

        # 判断是否到底或空白
        if current_page_content:
            if current_page_content == previous_page_content:
                print("\n页面内容与上次完全一致，已滑动到底部。")
                break
            empty_count = 0
            previous_page_content = list(current_page_content)
        else:
            empty_count += 1
            print(f"当前屏幕未解析到剪贴板内容 (重试 {empty_count}/3)...")
            if empty_count >= 3:
                print("连续 3 次未抓取到内容，抓取结束。")
                break

        # 向上滑动屏幕翻页
        d.swipe(0.5, 0.7, 0.5, 0.5, 1.5)
        # 给屏幕留足刷新时间，确保 XML 能拉取到新数据
        time.sleep(1.5)

    # 导出文件
    output_filename = "sogou_clipboard_export.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        for i, text in enumerate(extracted_texts, 1):
            f.write(f"--- 记录 {i} ---\n")
            f.write(text + "\n\n")

    print(f"\n提取完成！一共提取到 {len(extracted_texts)} 条内容。")
    print(f"数据已保存到当前目录下的: {output_filename}")

if __name__ == "__main__":
    export_sogou_clipboard()