
with open('骂谁实力派呢1.txt', 'w') as wfile:

    # 打开文件
    with open('骂谁实力派呢.txt', 'r') as file:
        # 逐行读取并打印
        lastTitleLine = ""
        for line in file.readlines():
            writeLIne = line
            # print(line.strip())  # 使用strip()方法去除每行末尾的换行符
            if "第" in line and "章" in line:
                lastTitleLine = line
                lastTitleLine = lastTitleLine[6:]
                lastTitleLine = lastTitleLine.replace("\n", "")
            
            if "骂谁实力派呢正文卷" in line:
                print(lastTitleLine)
                print(line)
                findPos = line.find(lastTitleLine)
                finLen = len(lastTitleLine)
                after_lastTitleLine = line[findPos+finLen:]
                print(after_lastTitleLine)
                writeLIne = after_lastTitleLine

            wfile.write(writeLIne)

            # break