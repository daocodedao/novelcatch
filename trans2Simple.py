import zhconv

# 读取文件内容
file_path = '华娱：我竟成了资本大佬.txt'
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        traditional_text = file.read()

    # 进行繁体到简体的转换
    simplified_text = zhconv.convert(traditional_text, 'zh-cn')

    # 将转换后的文本写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(simplified_text)

    print("转换完成，已保存到文件。")
except FileNotFoundError:
    print(f"文件 {file_path} 未找到。")
except Exception as e:
    print(f"发生错误: {e}")