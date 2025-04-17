import time
import re
from playwright.async_api import Playwright, async_playwright
import asyncio
from zhconv import convert
import random


browser = None
context = None
page = None
async def catchNovel(playwright, nextPagePre, url):
    global browser,context,page
    if not browser:
        browser = await playwright.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
    
    await page.goto(url)
    
    for i in range(10):
        # 重试次数 = 10
        try:
            # //*[@id="sticky-parent"]/div[2]/div[3]
            # //*[@id="sticky-parent"]/div[2]/div[3]
            titleNode = await page.query_selector('//*[@id="sticky-parent"]/div[2]/div[3]')
            title = await titleNode.text_content()
            title = convert(title, 'zh-cn')
            contentNode = await page.query_selector('//*[@class="content"]')
            contents = await contentNode.text_content()
            contents = convert(contents, 'zh-cn')

            # //*[@id="mm-5"]/div[2]/div/ul/li[2]/a
            nextNode = await page.query_selector('//*[@class="next-chapter"]')
            next_url = await nextNode.get_attribute("href")  #定义text变量接收a标签底下的href属性

            next_url = nextPagePre + next_url

            return title, contents, next_url
        except Exception as e:
            print(f"sleep 15s {e}")
            time.sleep(random.uniform(0, 4))
            await page.reload()

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
                    if len(title) > 0:
                        title = handle_title(title, index, bookTitle, oldTitle)
                        if len(title) > 0:
                            print(title)
                            oldTitle = title
                            index = index + 1
                            f.write(title)
                            f.write("\r\n") 

                    
                    contentList = contents.split("\n\n")
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
    "url":"https://czbooks.net/n/s6dooi/s66586kp?chapterNumber=6",
    "bookTitle":"新时代艺术家",
    "nextPagePreUrl":"https:",  # 下一页URL前缀
    "mode":"new",  # 模式
    "sectionIdx":1  # 起始章节索引
}
]
# driver = webdriver.Chrome()

for novel in novelList:
     asyncio.run(readOneNovel(bookTitle=novel["bookTitle"], 
                              url=novel["url"], 
                              nextPagePre = novel["nextPagePreUrl"], 
                              mode=novel["mode"],
                              startSection=novel["sectionIdx"]))
