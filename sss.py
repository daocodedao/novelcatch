

def count_strings_in_file(file_path, target_string):
   count = 0
   with open(file_path, 'r', encoding='utf-8') as file:
       for line in file:
           count += line.count(target_string)
   return count

nameStr="桂浩源,富察旻宁,崔恒瑜,闫梓坤,孙腾,林子霄,王思涵,张诗昀,李梓熙,冀凌霄,李文清,罗刘忻,邢俪凡,康书维,李羽嫣,雍彬蔚,潘祺诺,冯怡诺,尹芮涵,徐霂嫣,霍苒,李佩珊,杨修语,张昱忻,吕寿霆,王铭泽,刘昱仑,许明阳,张轩鸣,吴泓毅,戴子竣,任晓阳,杨弘毅,库可,龚梓宸,刘赫廷,王项,姚顺宇,贺建豪,李承泽"
# nameStr="国武武馆,双榆树一小,万泉小学,鼎石,北外附校,开心武道,尚武国际,人小亮甲店,人北实验,翰墨武林,涵飒武术,国艺"

nameList=nameStr.split(",")
file_path = '44.txt'  # 文件路径

outStr=""
for name in nameList:
    count = count_strings_in_file(file_path, name)
    print(f'"{name}"  {count}')
    outStr=f"{outStr},{count}"


print(outStr)


