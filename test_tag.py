import re


def addHashTag(input=""):
    if len(input) == 0:
        return ""
    hashwords = ['eth','bitcoin','btc','genesis']

    words = input.split()
    for word in words:
        if word[0] != '#':
            if word.lower() in hashwords:
                input = input.replace(" " + word, " #"+word)

    print(input)
    return input

def add_new_lines(text):  
    pattern = r'(\s*)第([0-9])章(\s*)'   
    result = re.sub(pattern, r'\n  第\2章\3', text)  
    return result
  
text = "这是第1章的内容，接下来是第1章的内容。"
new_text = add_new_lines(text)
print(new_text)