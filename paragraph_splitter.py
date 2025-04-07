import re
import os
import argparse

def split_long_paragraphs(text):
    """
    将过长的段落（超过3个句子）分割成更短的段落
    """
    paragraphs = text.split('\n')
    new_paragraphs = []
    
    for paragraph in paragraphs:
        # 跳过空段落或章节标题（通常以"第"开头的行）
        if not paragraph.strip() or paragraph.strip().startswith('第') and '章' in paragraph:
            new_paragraphs.append(paragraph)
            continue
            
        # 跳过已经很短的段落（少于50个字符）
        if len(paragraph.strip()) < 50:
            new_paragraphs.append(paragraph)
            continue
        
        # 处理双引号内的内容，暂时替换引号内的标点符号
        quote_blocks = re.findall(r'"[^"]*"', paragraph)
        placeholder_map = {}
        
        for i, block in enumerate(quote_blocks):
            placeholder = f"QUOTE_PLACEHOLDER_{i}"
            # 保存原始引号块和占位符的映射
            placeholder_map[placeholder] = block
            # 替换原文中的引号块为占位符
            paragraph = paragraph.replace(block, placeholder)
        
        # 使用正则表达式分割句子，考虑中文和英文的句号、问号、感叹号
        sentences = re.split(r'([。！？\.!?]+)', paragraph)
        # 将分割后的标点符号重新附加到句子上
        sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2] + [''])]
        sentences = [s for s in sentences if s.strip()]
        
        # 如果句子数量超过3，则进行分段
        if len(sentences) > 3:
            current_paragraph = []
            sentence_count = 0
            
            for sentence in sentences:
                current_paragraph.append(sentence)
                sentence_count += 1
                
                # 每3个句子形成一个新段落
                if sentence_count == 3:
                    paragraph_text = ''.join(current_paragraph)
                    # 恢复占位符为原始引号块
                    for placeholder, original in placeholder_map.items():
                        paragraph_text = paragraph_text.replace(placeholder, original)
                    new_paragraphs.append(paragraph_text)
                    current_paragraph = []
                    sentence_count = 0
            
            # 处理剩余的句子
            if current_paragraph:
                paragraph_text = ''.join(current_paragraph)
                # 恢复占位符为原始引号块
                for placeholder, original in placeholder_map.items():
                    paragraph_text = paragraph_text.replace(placeholder, original)
                new_paragraphs.append(paragraph_text)
        else:
            # 如果句子数量不超过3，保持原段落不变
            # 恢复占位符为原始引号块
            for placeholder, original in placeholder_map.items():
                paragraph = paragraph.replace(placeholder, original)
            new_paragraphs.append(paragraph)
    
    return '\n'.join(new_paragraphs)

def process_file(input_file, output_file=None):
    """
    处理输入文件并将结果写入输出文件
    """
    # 如果没有指定输出文件，则在输入文件名基础上添加后缀
    if output_file is None:
        file_name, file_ext = os.path.splitext(input_file)
        output_file = f"{file_name}_reformatted{file_ext}"
    
    try:
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # 处理文本
        processed_text = split_long_paragraphs(text)
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_text)
        
        print(f"处理完成！结果已保存到: {output_file}")
        return True
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        return False

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='将小说中过长的段落（超过3个句子）分割成更短的段落')
    # parser.add_argument('input_file', help='输入文本文件路径')
    # parser.add_argument('-o', '--output', help='输出文本文件路径（可选）')
    
    # args = parser.parse_args()
    input_file = "./我只想自力更生.txt"
    output = "./我只想自力更生1.txt"
    process_file(input_file, output)