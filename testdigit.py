def convert_number(s):
    num = int(s[1:-1])
    chinese_numbers = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    chinese_units = ['', '十', '百', '千']
    result = ''
    if num == 0:
        return chinese_numbers[0]
    while num > 0:
        digit = num % 10
        if digit > 0:
            result = chinese_numbers[digit] + chinese_units[0] + result
        elif len(result) > 0 and result[0]!= '零':
            result = chinese_numbers[digit] + result
        num //= 10
        if num > 0:
            unit_index = (len(str(num)) - 1) % 4
            if digit > 0:
                result = chinese_units[unit_index] + result
            else:
                result = chinese_units[unit_index] + '零' + result
    return result.strip('零')

with open('導演的快樂你不懂58.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

newLines = []
for line in lines:
    parts = line.split(' ')
    for i, part in enumerate(parts):
        if part.startswith('第') and part.endswith('章'):
            number = part[1:-1]
            chinese_number = convert_number(part)
            parts[i] = '第' + chinese_number + '章'
    new_line =' '.join(parts)
    # print(new_line)
    newLines.append(new_line)

with open('out.txt', 'w', encoding='utf-8') as f:
    f.writelines(newLines)