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

def handle_title(title, index, bookTitle, oldTitle):
    
    # 移除数字加括号或顿号的格式
    pattern = r"\d+\）"
    title = re.sub(pattern, "", title)
    
    # 移除从左括号开始到末尾的所有内容
    pattern = r'（.*|（.*|（.*$|\(.*|\(.*|\(.*$'
    title = re.sub(pattern, "", title)
    
    pattern = r"\d+\、"
    title = re.sub(pattern, "", title)

    # 处理数字加点加"第"的格式，如"1.第"
    pattern = r'(\d+)\.第'
    title = re.sub(pattern, "第", title)

    # 移除书名和特殊格式
    title = title.replace(f"《{bookTitle}》", "")
    title = title.replace(bookTitle, "")
    title = title.replace("_", "")
    title = title.replace("正文 ", "")
    title = title.replace("\xa0", "")
    title = title.replace("1）分段阅读_", "")
    title = title.replace("章  ", "章 ")
    

    # 处理中文数字或阿拉伯数字加空格加标题的情况
    # 匹配模式：数字（中文或阿拉伯）+ 空格 + 标题
    chinese_number_pattern = r'^([零一二三四五六七八九十百千万]+)\s+(.+)$'
    arabic_number_pattern = r'^(\d+)\s+(.+)$'
    
    # 处理中文数字的情况，如"一 初来乍到" -> "第1章 初来乍到"
    match = re.match(chinese_number_pattern, title.strip())
    if match:
        try:
            number = chinese_to_arabic(match.group(1))
            title = f"第{number}章 {match.group(2)}"
        except:
            pass
    
    # 处理阿拉伯数字的情况，如"1 初来乍到" -> "第1章 初来乍到"
    match = re.match(arabic_number_pattern, title.strip())
    if match:
        number = match.group(1)
        title = f"第{number}章 {match.group(2)}"

    # 处理已有的"第xxx章"格式（将中文数字转换为阿拉伯数字）
    def convert_numbers(match):
        chinese_num = match.group(1)
        try:
            number = chinese_to_arabic(chinese_num)
            return f"第{number}章"
        except:
            return match.group(0)

    # 匹配并转换"第xxx章"中的中文数字
    pattern = r'第([零一二三四五六七八九十百千万]+)章'
    title = re.sub(pattern, convert_numbers, title)
    
    # 处理重复标题和标准化章节格式
    if title == oldTitle or title in oldTitle:
        title = ""    
    else:
        if "章" not in title:
            # 如果标题中没有"章"字，添加标准章节格式
            title = f"第{index}章 {title}"
        else:
            # 标准化章节标题的空格
            title = title.replace("章", "章 ")
            title = title.replace("章  ", "章 ")

    # 只保留从"第"字开始的标题部分
    position = title.find("第")
    if position != -1:
        title = title[position:]

    # 移除分段阅读标记
    if "分段阅读" in title:
        title = ""
    
    # 移除标题中的特殊标记
    # 处理中英文括号及其后面的内容
    title = re.sub(r'（[^）]*）', '', title)  # 移除中文括号及其中的内容
    title = re.sub(r'\([^\)]*\)', '', title)  # 移除英文括号及其中的内容
    
    return title

def handle_content(content):
    retStr = ""
    content = content.replace("\r\n", "")
    
    content = content.replace("\xa0\xa0\xa0\xa0", "")
    pattern = r'第\d+章'
    if re.search(pattern, content):
        return retStr
    if "第" in content and "章" in content:
        return retStr
    if "分段阅读" in content:
        return retStr

    content = content.replace("\u3000\u3000", "")
    content = content.replace("\n\u2003\u2003", "")
    content = content.replace("\u2003", "")
    content = content.replace("（求月票）", "")
    content = content.replace("（求收藏）", "")
    content = content.replace("\n\t", "")
    content = content.replace("\n", "")
    content = content.replace("            ", "")
    if "本章未完，点击下一页继续阅读" in content:
        content = ""
    if "本章完" in content:
        content = ""
    
    
    retStr = content
    return retStr
