
import pandas as pd
import json

sheetArray=["小学男子乙组","小学女子乙组","小学男子甲组","小学女子甲组"]
outStr=""
for sheetname in sheetArray:
    file_path = 'source.xlsx'  # 文件路径
    df = pd.read_excel(file_path, sheet_name=sheetname, engine='openpyxl')

    outstr=sheetname

    nameArray = []
    for column in df.columns:
        if column=="序号" or column == "项目":
            continue
        else:
            nameArray.append(column)


    # Convert excel to string 
    # (define orientation of document in this case from up to down)
    thisisjson = df.to_json(orient='records', force_ascii=False)

    # Print out the result
    # print('Excel Sheet to JSON:\n', thisisjson)

    array = json.loads(thisisjson)

    eachTypeStr=""
    for oobject in array:
        stype = oobject["项目"]
        if "太极" in stype:
            continue

        eachTypeStr=f"{outstr}{stype}"
        for name in nameArray:
            isJoin=oobject[name]
            if isJoin==1.0:
                name=name.replace(" ","")
                name=name.replace(" ","")

                if "," in eachTypeStr:
                    eachTypeStr=f"{eachTypeStr}	{name}"
                else:
                    eachTypeStr=f"{eachTypeStr}	{name}"


        if len(outStr)==0:
            outStr=f"{eachTypeStr}"
        else:
            outStr=f"{outStr}\n{eachTypeStr}"


with open('out.txt', 'w', encoding='utf-8') as file:
  # 将字符串写入文件
  file.write(outStr)