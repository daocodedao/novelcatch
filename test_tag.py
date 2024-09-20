import re

def replace_string(string):
    """
    替换字符串，提取章数和标题

    Args:
        string: 待替换的字符串

    Returns:
        替换后的字符串
    """

    # 正则表达式匹配章数和标题
    pattern = r"(\d+)\.第\1章 (.*)"
    match = re.match(pattern, string)

    if match:
        chapter_num, title = match.groups()
        return f"第 {chapter_num} 章 {title}"
    else:
        return "格式错误"

# 测试用例
strings = [
    "90.第90章 姐姐就是那路边的野花",
    "291.第291章 姐姐就是那路边的野花2",
    "2392.第2392章 姐姐就是那路边的野花3"
]

for string in strings:
    result = replace_string(string)
    print(result)