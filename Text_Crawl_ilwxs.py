import time
import re
from playwright.async_api import Playwright, async_playwright
import asyncio
from zhconv import convert
import random
from textUtil import chinese_to_arabic, handle_title,handle_content

MaxSleepSecond = 1
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
            titleNode = await page.query_selector('//*[@class="headline"]')
            title = await titleNode.text_content()
            # title = convert(title, 'zh-cn')
            contentNode = await page.query_selector('//*[@class="content"]')
            contents = await contentNode.text_content()
            # contents = convert(contents, 'zh-cn')


            nextNode = await page.query_selector('//*[@class="pager"]/a[3]')
            next_url = await nextNode.get_attribute("href")  #定义text变量接收a标签底下的href属性

            next_url = nextPagePre + next_url

            return title, contents, next_url
        except Exception as e:
            print(f"sleep 15s {e}")
            time.sleep(random.uniform(0, MaxSleepSecond))
            await page.reload()



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

                    
                    contentList = contents.split(" ")
                    for content in contentList:
                        content = handle_content(content)
                        if len(content) == 0:
                            continue
                        f.write(content)
                        f.write("\r\n") 

                    time.sleep(random.uniform(0, MaxSleepSecond))
                    title, contents, next_url = await catchNovel(playwright, nextPagePre, next_url)
            except Exception as e:
                print(e)
                f.close() 

novelList=[
{
    "url":"https://m.ilwxs.com/shu/73314/143818864.html",
    "bookTitle":"华娱2000：大唐诗仙",
    "nextPagePreUrl":"https://m.ilwxs.com",  # 下一页URL前缀
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
