import re

def check_english_in_file(file_path):
  with open(file_path, 'r', encoding='utf-8') as f:
      content = f.read()
      english_pattern = re.compile(r'[a-zA-Z]+')
      english_list = english_pattern.findall(content)
      for english_word in english_list:
          print(f"文件 {file_path} 包含英文字符：{english_word}")
         #  return True
  return False


file_path = "./美艳教师.txt"
if check_english_in_file(file_path):
   print(f"文件 {file_path} 包含拼音")
else:
   print(f"文件 {file_path} 不包含拼音")