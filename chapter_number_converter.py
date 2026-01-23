import re

def chinese_to_arabic(chinese_num):
    """将中文数字转换为阿拉伯数字"""
    cn_num = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '十': 10, '百': 100, '千': 1000, '万': 10000
    }
    
    result = 0
    tmp = 0
    unit = 1
    
    # 反转字符串
    chinese_num = chinese_num[::-1]
    
    for char in chinese_num:
        if char in ['十', '百', '千', '万']:
            unit = cn_num[char]
            if tmp == 0:
                tmp = 1
        elif char in cn_num:
            tmp = cn_num[char]
            result += tmp * unit
            tmp = 0
    
    if tmp != 0:
        result += tmp
        
    return result

def convert_chapter_numbers(text):
    """转换章节标题中的中文数字为阿拉伯数字"""
    def replace_match(match):
        chapter_text = match.group(0)
        # 提取中文数字部分
        number_text = chapter_text[1:-1]  # 去掉"第"和"章"
        try:
            arabic_number = chinese_to_arabic(number_text)
            return f"第{arabic_number}章"
        except:
            return chapter_text
    
    # 匹配"第xxx章"格式的文本
    pattern = r'第[零一二三四五六七八九十百千万]+章'
    return re.sub(pattern, replace_match, text)


def process_file(input_file, output_file='out.txt'):
    """处理输入文件并将结果写入输出文件"""
    try:
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 转换章节编号
        converted_content = convert_chapter_numbers(content)
        converted_content = convert_chapter_numbers(content)
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(converted_content)
            
        print(f"处理完成！结果已保存到: {output_file}")
        return True
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        return False

if __name__ == "__main__":
    input_file = "决胜新金融时代.txt"
    process_file(input_file)