import re
def divide_paragraphs(text):
    paragraphs = text.split("\n")
    result = []
    for paragraph in paragraphs:
        sentences = []
        current_sentence = ""
        for char in paragraph:
            current_sentence += char
            if char in ["。", "？", "！"]:
                sentences.append(current_sentence)
                current_sentence = ""
        if current_sentence:
            sentences.append(current_sentence)
            
        if len(sentences) <= 10:
            result.append(paragraph)
        else:
            groups = [sentences[i:i + 5] for i in range(0, len(sentences), 5)]
            for group in groups:
                result.append("".join(group))

    return result

# 读取文件内容
file_path = '超神级学霸.txt'  # 替换为你的文件路径
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# 分割段落
paragraphs = divide_paragraphs(text)

# 将结果保存到新文件
output_file_path = '超神级学霸s.txt'  # 替换为输出文件路径
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write('\n\n'.join(paragraphs))