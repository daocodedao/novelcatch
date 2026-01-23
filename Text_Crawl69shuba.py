
import time
import re
import asyncio
from playwright.async_api import async_playwright
import random

browser = None
context = None
page = None

def replace_string(string):
    """
    替换字符串，提取章数和标题

    Args:
        string: 待替换的字符串

    Returns:
        替换后的字符串
    """

    # 正则表达式匹配章数和标题
    pattern = r"(\d+)\.第\1章 (.*)"
    match = re.match(pattern, string)

    if match:
        chapter_num, title = match.groups()
        return f"第 {chapter_num} 章 {title}"
    else:
        return string


async def catchNovel(playwright, nextPagePre, url):
    global browser,context,page
    if not browser:
        browser = await playwright.chromium.launch(headless=False, executable_path="/Users/linzhiji/Library/Caches/ms-playwright/chromium-1155/chrome-mac/Chromium.app/Contents/MacOS/Chromium")
        
        
        context = await browser.new_context()
        page = await context.new_page()
    await page.goto(url)
    
    for i in range(10):
        # 重试次数 = 10
        try:
            titleNode = await page.query_selector('//*[@class="hide720"]')
            title = await titleNode.text_content()
            if len(title.split("（")) > 0:
                title = title.split("（")[0]
            title = replace_string(title)

            contentNode = await page.query_selector('//*[@class="txtnav"]')
            contents = await contentNode.text_content()

            nextNode = await page.query_selector('//*[@class="page1"]/a[4]')
            next_url = await nextNode.get_attribute("href")  #定义text变量接收a标签底下的href属性

            # next_url = nextPagePre + next_url
            # next_url = "https://m.qmxs123.com" + next_url
            return title, contents, next_url
        except Exception as e:
            print(e)
            time.sleep(1)
            await page.reload()
            


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
    content = content.replace("\u2003\u2003", "")
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

                    contentList = contents.split("\u2003\u2003")
                    for content in contentList:
                        content = handle_content(content)
                        if len(content) == 0:
                            continue
                        f.write(content)
                        f.write("\r\n") 

                    time.sleep(random.uniform(0, 4))
                    title, contents, next_url = await catchNovel(playwright, nextPagePre, next_url)
            except Exception as e:
                print(e)
                f.close() 

novelList=[
{
    "url":"https://www.69shuba.com/txt/67131/38434419",
    "bookTitle":"华娱2017：从顶流作家开始",
    "nextPagePreUrl":"https://69shuba.com",
    "mode":"new",
    "sectionIdx":1
}
]

for novel in novelList:
    asyncio.run(readOneNovel(novel["bookTitle"], 
                             novel["url"], 
                             nextPagePre = novel["nextPagePreUrl"], 
                             mode=novel["mode"],
                             startSection=novel["sectionIdx"]))