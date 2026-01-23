import time
import re
from playwright.async_api import Playwright, async_playwright

import asyncio
from zhconv import convert
import random
from textUtil import chinese_to_arabic, handle_title, handle_content


browser = None
context = None
page = None
async def catchNovel(playwright, nextPagePre, url):
    global browser, context, page
    if not browser:
        # browser = await playwright.firefox.launch(headless=False)
        browser = await playwright.chromium.launch(headless=False, executable_path="/Users/linzhiji/Library/Caches/ms-playwright/chromium-1155/chrome-mac/Chromium.app/Contents/MacOS/Chromium")
        context = await browser.new_context()
        page = await context.new_page()
    
    await page.goto(url, timeout=60000)
    
    for i in range(10):
        # 重试次数 = 10
        try:
            # TODO: 判断页面里是否有<button> 标签里的文案是  加|载|更|多 ，如果有就点击
            # 查找文案包含"加载更多"的按钮并点击
            load_more_button = await page.query_selector('button:text("加|载|更|多"), button:has-text("加|载|更|多"), *[role="button"]:text("加|载|更|多"), div:text("加|载|更|多")')
            if load_more_button:
                await load_more_button.click()
                # 等待可能的内容加载
                await page.wait_for_timeout(2000)
            
            titleNode = await page.query_selector('//*[@id="main"]/h1')
            title = await titleNode.text_content()
            title = convert(title, 'zh-cn')
            contentNode = await page.query_selector('//*[@class="content"]')
            contents = await contentNode.text_content()
            contents = convert(contents, 'zh-cn')

            # //*[@id="mm-5"]/div[2]/div/ul/li[2]/a
            nextNode = await page.query_selector('//*[@class="page"]/div[3]/a')
            next_url = await nextNode.get_attribute("href")  #定义text变量接收a标签底下的href属性

            next_url = nextPagePre + next_url

            return title, contents, next_url
        except Exception as e:
            print(f"sleep 15s {e}")
            time.sleep(random.uniform(0, 4))
            await page.reload()


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
    "url":"https://m.qbmfxs.com/book_1/69365/534",
    "bookTitle":"华娱扛把子",
    "nextPagePreUrl":"https://m.qbmfxs.com/",  # 下一页URL前缀
    "mode":"add",  # 模式
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