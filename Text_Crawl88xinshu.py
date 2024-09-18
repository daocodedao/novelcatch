
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


def catchNovel(url):
    
    driver.get(url)

    while driver.execute_script("return document.readyState") != "complete":
        time.sleep(1)

    text = driver.page_source  

    html = etree.HTML(text)

    title = html.xpath('//*[@id="nr_title"]/text()')[0]
    contents:list[str] = html.xpath('//*[@id="nr1"]/p/text()')
    # a[0]/@href
    # /html/body/div[1]/div[4]/div[1]/ul/li[3]/a
    # next_url = html.xpath('//*[@class="page1"]/@href')
    next_url = html.xpath('//*[@id="pt_next"]/@href')[0]

    # https://m.88xinshu.com/book/332/332830/104022192_2.html
    # https://m.88xinshu.com/book/332/332830/104022192_2.html
    next_url = "https://m.88xinshu.com" + next_url
    # next_url = "https://m.qmxs123.com" + next_url
    # if "_" not in url:
    #     title = contents[0]
    #     contents.remove(contents[0])
    # else:
    #     title = ""
    return title, contents, next_url


def handle_title(title, index, bookTitle, oldTitle):
    title = title.replace("（求月票）", "")
    title = title.replace("（求收藏）", "")
    
    pattern = r"\d+\）"
    title = re.sub(pattern, "", title)
    pattern = r"\d+\、"
    title = re.sub(pattern, "", title)

    pattern = r'(\d+)\.第'
    title = re.sub(pattern, "第", title)


    title = title.replace(bookTitle, "")
    title = title.replace("_", "")
    title = title.replace("正文 ", "")
    title = title.replace("1）分段阅读_", "")
    title = title.replace("章  ", "章 ")

    # title = cn2an.transform(title, "cn2an")

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
    content = content.replace("（求月票）", "")
    content = content.replace("（求收藏）", "")
    content = content.replace("\n\t", "")
    content = content.replace("\n", "")
    content = content.replace("            ", "")
    if "本章未完，点击下一页继续阅读" in content:
        content = ""
    if "本章完" in content:
        content = ""
    
    
    retStr = content
    return retStr

def readOneNovel(bookTitle, url, mode="complete"):
    oldTitle = ""
    index = 1
    # 覆盖写
    writeMode = 'w' 
    if mode == "add":
        # 追加写
        writeMode = 'a'
    
    with open(bookTitle + '.txt', writeMode, encoding='utf-8') as f:
        try:
            title, contents, next_url = catchNovel(url)
            while(1):
                if len(title) > 0:
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
                title, contents, next_url = catchNovel(next_url)
        except Exception as e:
            print(e)
            f.close() 

novelList=[
{
    "url":"https://m.88xinshu.com/book/273/273114/94865233.html",
    "bookTitle":"剥削好莱坞1980",
    "mode":"new"
}
]
driver = webdriver.Chrome()
for novel in novelList:
    readOneNovel(novel["bookTitle"], novel["url"], novel["mode"])

# start_time = time.time()    
# threads = [] 
# for novel in novelList:
#     th = threading.Thread(target=readOneNovel, args=(novel["bookTitle"], novel["url"]))
#     th.start()
#     # threads.append(th)        

#     # readOneNovel(novel["bookTitle"], novel["url"])
# # for th in threads:
# #     th.join() # Main thread wait for threads finish
    
# # print("multiple threads took ", (time.time() - start_time), " seconds")
# # for _ in range(4):
# #    threading.Thread(tagret=main).start()