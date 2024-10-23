
import time
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import cn2an

from lxml import etree
import threading

# https://blog.csdn.net/m0_58086930/article/details/128667573

def catchList(url):
    driver.get(url)

    while driver.execute_script("return document.readyState") != "complete":
        time.sleep(1)

    text = driver.page_source  

    html = etree.HTML(text)

    listChapter = html.xpath('/html/body/div[2]/div[2]/div/div/div[2]/ul/li')

    chapterInfoList = []
    cha = {}
    for chapter in listChapter:
        cha["chapterName"] = chapter.xpath('./a/text()')[0]
        cha["chapterUrl"] = f"http://www.xianqihaotianmi.org{chapter.xpath('./a/@href')[0]}"
        chapterInfoList.append(cha.copy())
    return chapterInfoList

def catchNovel(url):
    
    driver.get(url)

    while driver.execute_script("return document.readyState") != "complete":
        time.sleep(1)

    text = driver.page_source  
    html = etree.HTML(text)
    # title = html.xpath('//*[@class="title"]/text()')[0]
    # contents = html.xpath('//div[@class="content-body"]/text()')
    contents = html.xpath('/html/body/div[2]/div[1]/div/div[2]/div[3]/text()')
    return contents


def handle_title(title, index, bookTitle, oldTitle):
    pattern = r"\d+\）"
    title = re.sub(pattern, "", title)
    pattern = r"\d+\、"
    title = re.sub(pattern, "", title)

    title = title.replace(bookTitle, "")
    title = title.replace("_", "")
    title = title.replace("正文 ", "")
    title = title.replace("1）分段阅读_", "")
    title = title.replace("章  ", "章 ")
    title = title.replace("、", "")
    title = title.replace("（求收藏）", "")
    title = title.replace("（求订阅）", "")
    title = title.replace("（求保底月票）", "")
    title = title.replace("（求月票）", "")
    
    
    title = cn2an.transform(title, "cn2an")

    if title == oldTitle or title in oldTitle:
        title = ""    
    else:
        if "章" not in title:
            title = f"第{index}章 {title}"
        else:
            title = title.replace("章", "章 ")
            title = title.replace("章  ", "章 ")

    position = title.find("第")
    if position != -1:
        title = title[position:]

    if "分段阅读" in title:
        title = ""
    
    return title

def handle_content(content):
    retStr = ""
    content = content.replace("\r\n", "")
    content = content.replace("\xa0\xa0\xa0\xa0", "")
    pattern = r'第\d+章'
    if re.search(pattern, content):
        return retStr
    if "第" in content and "章" in content:
        return retStr
    if "分段阅读" in content:
        return retStr

    content = content.replace("\u3000\u3000", "")
    content = content.replace("\n\u2003\u2003", "")
    content = content.replace("请收藏：https://m.qmxs123.com", "")
    content = content.replace("温梦卿李小兵老黄", "")
    content = content.replace("\n\t", "")
    content = content.replace("\n", "")
    content = content.replace("            ", "")
    content = content.replace("(本章完)", "")
    
    retStr = content
    return retStr

def readOneNovel(bookTitle, url, listUrl, mode="complete"):
    oldTitle = ""
    index = 1
    # 覆盖写
    writeMode = 'w' 
    if mode == "add":
        # 追加写
        writeMode = 'a'
    
    with open(bookTitle + '.txt', writeMode, encoding='utf-8') as f:
        try:
            chapterInfoList = catchList(listUrl)
            for chapterInfo in chapterInfoList:
                title = chapterInfo["chapterName"]
                contents= catchNovel(chapterInfo["chapterUrl"])
                
                title = handle_title(title, index, bookTitle, oldTitle)
                if len(title) > 0:
                    print(title)
                    oldTitle = title
                    index = index + 1
                    f.write(title)
                    f.write("\r\n") 

                
                for content in contents:
                    content = handle_content(content)
                    if len(content) == 0:
                        continue
                    f.write(content)
                    f.write("\r\n") 

                time.sleep(0.3)
        except Exception as e:
            print(e)
            f.close() 

novelList=[
{
    "url":"http://www.xianqihaotianmi.org/read/104723_44942672.html",
    "listUrl":"http://www.xianqihaotianmi.org/book/104723.html",
    "bookTitle":"超神级学霸",
    "mode":"new"
},

]
driver = webdriver.Chrome()
for novel in novelList:
    readOneNovel(novel["bookTitle"], novel["url"], novel["listUrl"], novel["mode"])

