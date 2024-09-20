
import time
# from selenium import webdriver
import os
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
import re
from playwright.async_api import Playwright, async_playwright
import threading
import asyncio
from zhconv import convert

os.environ['HTTP_PROXY'] = "127.0.0.1:10809"
os.environ['HTTPS_PROXY'] = "127.0.0.1:10809"

browser = None
context = None
page = None
async def catchNovel(playwright, url):
    global browser,context,page
    if not browser:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
    await page.goto(url)

    # //*[@id="sticky-parent"]/div[2]/div[3]
    # //*[@id="sticky-parent"]/div[2]/div[3]
    titleNode = await page.query_selector('//*[@class="bookname"]')
    title = await titleNode.text_content()
    if len(title.split("（")) > 0:
        title = title.split("（")[0]

    p_tags  = await page.query_selector_all('//*[@id="booktxt"]/p')
    all_contents=""
    for p_tag in p_tags:
        # 获取<p>标签下的文字内容
        text_content = await p_tag.text_content()

        if "章 " in text_content and len(all_contents) == 0:
            title = text_content
            if len(title.split("（")) > 0:
                title = title.split("（")[0]
            continue

        # 将文字内容添加到列表中
        all_contents=f"{all_contents}\n{text_content}"
    contents = all_contents

    # //*[@id="mm-5"]/div[2]/div/ul/li[2]/a
    nextNode = await page.query_selector('//*[@class="bottem2"]/a[3]')
    next_url = await nextNode.get_attribute("href")  #定义text变量接收a标签底下的href属性


    next_url = "https://xszj.org" + next_url

    return title, contents, next_url

def handle_title(title, index, bookTitle, oldTitle:str):
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
    if "章 " in oldTitle:
        splitTitle = oldTitle[oldTitle.find("章 ")+2:]
        if splitTitle in title:
            title = ""
            return title

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
    content = content.replace("\u2003", "")
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

async def readOneNovel(bookTitle, url, mode="complete"):
    oldTitle = ""
    index = 1
    # 覆盖写
    writeMode = 'w' 
    if mode == "add":
        # 追加写
        writeMode = 'a'
    async with async_playwright() as playwright:
        with open(bookTitle + '.txt', writeMode, encoding='utf-8') as f:
            try:
                title, contents, next_url = await catchNovel(playwright, url)
                while(1):
                    if len(title) > 0:
                        title = handle_title(title, index, bookTitle, oldTitle)
                        if len(title) > 0:
                            print(title)
                            oldTitle = title
                            index = index + 1
                            f.write(title)
                            f.write("\r\n") 

                    
                    contentList = contents.split("\n")
                    for content in contentList:
                        content = handle_content(content)
                        if len(content) == 0:
                            continue
                        f.write(content)
                        f.write("\r\n") 

                    time.sleep(0.3)
                    title, contents, next_url = await catchNovel(playwright, next_url)
            except Exception as e:
                print(e)
                f.close() 

novelList=[
{
    "url":"https://xszj.org/b/372215/c/11796385",
    "bookTitle":"黄金时代1990",
    "mode":"add"
}
]
# driver = webdriver.Chrome()

for novel in novelList:
     asyncio.run(readOneNovel(novel["bookTitle"], novel["url"], novel["mode"]))
