import os
import io


# 第1章 1）第1节 宿醉
# 第8章 2）第4节 5个孤儿1个光棍爹

def skipSpec():
    # 指定要读取的文件路径
    read_file_path = "大时代从1983开始.txt"
    write_file_path = "out.txt"
    # 打开文件,以二进制模式读取
    with open(read_file_path, "r") as file_r:
        with open(write_file_path, "w") as file_w:
            # 遍历文件的每一行
            bIsFindSymbol = False
            oldTitle = ""
            for line in file_r:
                if "第" in line and "章" in line and "节" in line and "）" in line:
                    position = line.find("）")
                    if position != -1:
                        line = line[position+1:]
                    line = line.replace("节", "章")
                    if oldTitle == line:
                        line = ""
                    else:
                        oldTitle = line

                
                if len(line) > 0:
                    # 将这一行写入内存中的文件对象
                    file_w.write(line)

def printSection():
    read_file_path = "out.txt"
    # 打开文件,以二进制模式读取
    with open(read_file_path, "r") as file_r:
        # 遍历文件的每一行
        for line in file_r:
            if "第" in line and "章" in line:
                print(line)

# printSection()
skipSpec()