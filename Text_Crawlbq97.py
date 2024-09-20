
import time
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import cn2an
import asyncio
from playwright.async_api import Playwright, async_playwright

from lxml import etree
import threading

browser = None
context = None
page = None

async def catchNovel(playwright, nextPagePre, url):
    global browser,context,page
    if not browser:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
    await page.goto(url)
    

    titleNode = await page.query_selector('//*[@class="title"]')
    title = await titleNode.text_content()
    contentNode = await page.query_selector('//*[@id="chaptercontent"]')
    contents = await contentNode.text_content()
    # a[0]/@href
    # /html/body/div[1]/div[4]/div[1]/ul/li[3]/a
    # next_url = html.xpath('//*[@class="page1"]/@href')
    next_url_node = await page.query_selector('//*[@id="pb_next"]')
    next_url = await next_url_node.get_attribute("href")

    next_url = nextPagePre + next_url
    # next_url = "https://m.qmxs123.com" + next_url
    return title, contents, next_url


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
    retStr = content
    return retStr

async def readOneNovel(bookTitle, 
                       url, 
                       nextPagePre,
                       mode="complete",
                       startSection=1):
    oldTitle = ""
    index = startSection
    # 覆盖写
    writeMode = 'w' 
    if mode == "add":
        # 追加写
        writeMode = 'a'
    
    async with async_playwright() as playwright:
        with open(bookTitle + '.txt', writeMode, encoding='utf-8') as f:
            try:
                title, contents, next_url = await catchNovel(playwright, nextPagePre, url)
                while(1):
                    title = handle_title(title, index, bookTitle, oldTitle)
                    if len(title) > 0:
                        print(title)
                        oldTitle = title
                        index = index + 1
                        f.write(title)
                        f.write("\r\n") 

                    contentList = contents.split("\u3000\u3000")
                    for content in contentList:
                        content = handle_content(content)
                        if len(content) == 0:
                            continue
                        f.write(content)
                        f.write("\r\n") 

                    time.sleep(0.3)
                    title, contents, next_url = await catchNovel(playwright, nextPagePre, next_url)
            except Exception as e:
                print(e)
                f.close() 

novelList=[
{
    "url":"https://www.bq97.cc/htm/35090/87.html",
    "bookTitle":"匠心",
    "nextPagePreUrl":"https://www.bq97.cc",
    "mode":"add",
    "sectionIdx":87
}
]

for novel in novelList:
    asyncio.run(readOneNovel(novel["bookTitle"], 
                             novel["url"], 
                             nextPagePre = novel["nextPagePreUrl"], 
                             mode=novel["mode"],
                             startSection=novel["sectionIdx"]))