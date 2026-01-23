import time
import re
from playwright.async_api import Playwright, async_playwright
import asyncio
from zhconv import convert
import random
from textUtil import chinese_to_arabic, handle_title,handle_content


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

            # titleNode = await page.query_selector('//*[@id="sticky-parent"]/div[2]/div[3]')
            # title = await titleNode.text_content()
            
            titleNode = await page.query_selector('//*[@class="title"]')
            title = await titleNode.text_content()
            title = convert(title, 'zh-cn')
            
            contentNode = await page.query_selector('//*[@class="content"]')
            contents = await contentNode.text_content()
            contents = convert(contents, 'zh-cn')

            # //*[@id="mm-5"]/div[2]/div/ul/li[2]/a
            nextNode = await page.query_selector('//*[@class="section-opt"]/a[4]')
            next_url = await nextNode.get_attribute("href") 
            

            next_url = nextPagePre + next_url

            return title, contents, next_url
        except Exception as e:
            print(f"sleep 15s {e}")
            # time.sleep(random.uniform(0, 1))
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

                    
                    contentList = contents.split("\u3000\u3000\u3000\u3000")
                    for content in contentList:
                        if "read2()" in content:
                            continue
                        content = handle_content(content)
                        if len(content) == 0:
                            continue
                        f.write(content)
                        f.write("\r\n") 

                    # time.sleep(random.uniform(0, 1))
                    title, contents, next_url = await catchNovel(playwright, nextPagePre, next_url)
            except Exception as e:
                print(e)
                f.close() 

novelList=[
{
    "url":"http://23.224.242.59/book/114948/44874047.html",
    "bookTitle":"华娱之娱乐时代",
    "nextPagePreUrl":"http://23.224.242.59",  # 下一页URL前缀
    "mode":"add",  # 模式
    "sectionIdx":363  # 起始章节索引
}
]
# driver = webdriver.Chrome()

for novel in novelList:
     asyncio.run(readOneNovel(bookTitle=novel["bookTitle"], 
                              url=novel["url"], 
                              nextPagePre = novel["nextPagePreUrl"], 
                              mode=novel["mode"],
                              startSection=novel["sectionIdx"]))
