
import time
import re
import asyncio
from playwright.async_api import Playwright, async_playwright
from textUtil import chinese_to_arabic, handle_title, handle_content

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
    "url":"https://www.sad4.cc/book/60959/660.html",
    "bookTitle":"重生从闲鱼赢起",
    "nextPagePreUrl":"https://www.sad4.cc",
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