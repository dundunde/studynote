import uiautomator2 as u2

def x_ray_screen():
    print("正在连接设备...")
    d = u2.connect()
    
    print("\n请在 5 秒内打开手机，呼出搜狗【剪贴板】界面...")
    import time
    time.sleep(5)
    
    print("\n--- 正在给屏幕拍 X 光 ---")
    
    # 1. 查看当前活动的 App 包名
    current_app = d.app_current()
    print(f"当前 Python 认为自己在看这个 App: {current_app}")
    
    # 2. 导出当前屏幕的纯文本结构（底层 XML）
    xml_content = d.dump_hierarchy()
    with open("ui_skeleton.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)
    print("已将屏幕底层骨架保存为: ui_skeleton.xml")
    
    # 3. 暴力打印屏幕上的所有文字（不加任何过滤）
    print("\n--- Python 能够识别到的文字如下 ---")
    elements = d(className="android.widget.TextView")
    count = 0
    for elem in elements:
        try:
            # 尝试获取文字，不管是啥都打印出来
            text = elem.info.get('text', '')
            if text.strip():
                print(f"找到文字: {text}")
                count += 1
        except Exception as e:
            print(f"读取某个元素时报错: {e}")
            
    print(f"\n诊断结束！一共看到了 {count} 段文字。")

if __name__ == "__main__":
    x_ray_screen()