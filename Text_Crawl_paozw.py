
import time
import re
from playwright.async_api import async_playwright
import asyncio

# 全局变量，用于存储浏览器、上下文和页面对象
browser = None
context = None
page = None

async def catchNovel(playwright, nextPagePre, url):
    """
    抓取小说内容的函数
    
    参数:
    playwright - playwright实例
    nextPagePre - 下一页URL的前缀
    url - 当前页面URL
    
    返回:
    title - 章节标题
    contents - 章节内容
    next_url - 下一页URL
    """
    global browser,context,page
    if not browser:
        # 如果浏览器未初始化，则创建新的浏览器实例
        browser = await playwright.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
    await page.goto(url)

    for i in range(10):
        # 重试次数 = 10
        try:
            # 获取标题节点
            titleNode = await page.query_selector('//*[@class="title"]')
            title = await titleNode.text_content()
            # title = title.replace("正文卷  ", "")
            # title = title.replace("加入书签投票", "")
            
            # 获取内容节点
            contentNode = await page.query_selector('//*[@class="articlecon"]')
            contents = await contentNode.text_content()
            
            # 获取下一页链接
            nextNode = await page.query_selector('//*[@class="nr_page"]/a[3]')
            next_url = await nextNode.get_attribute("href")  #定义text变量接收a标签底下的href属性

            # 拼接完整的下一页URL
            next_url = f"{nextPagePre}{next_url}"
            return title, contents, next_url
        except Exception as e:
            print(e)
            time.sleep(1)
            await page.reload()
            
    

def handle_title(title, index, bookTitle, oldTitle):
    """
    处理章节标题，去除不需要的内容并格式化
    
    参数:
    title - 原始标题
    index - 章节索引
    bookTitle - 书名
    oldTitle - 上一章标题
    
    返回:
    处理后的标题
    """

    # 移除行末尾的中文小括号和英文小括号内的内容（包括括号）
    title = re.sub(r'（[^）]*）', '', title)  # 移除中文小括号及其内容
    title = re.sub(r'\([^\)]*\)', '', title)  # 移除英文小括号及其内容
    
    title = title.replace(bookTitle, "")
    # 检查是否与上一章标题相同
    if title == oldTitle or title in oldTitle:
        title = ""    
    else:
        # 标准化章节格式
        if "章" not in title:
            title = f"第{index}章 {title}"
        else:
            title = title.replace("章", "章 ")
            title = title.replace("章  ", "章 ")

    # 确保标题从"第"字开始
    position = title.find("第")
    if position != -1:
        title = title[position:]

    # 如果标题包含"分段阅读"，则清空标题
    if "分段阅读" in title:
        title = ""
    
    return title

def handle_content(content):
    """
    处理章节内容，去除不需要的内容和格式
    
    参数:
    content - 原始内容
    
    返回:
    处理后的内容
    """
    retStr = ""
    # 移除回车换行
    content = content.replace("\r\n", "")
    
    # 移除特定格式和空格
    content = content.replace("\xa0\xa0\xa0\xa0", "")
    
    # 检查内容是否包含章节标题，如果是则返回空字符串
    pattern = r'第\d+章'
    if re.search(pattern, content):
        return retStr
    if "第" in content and "章" in content:
        return retStr
    if "分段阅读" in content:
        return retStr

    # 清理各种空格和特殊字符
    content = content.replace("\u3000\u3000", "")
    content = content.replace("\n\u2003\u2003", "")
    content = content.replace("\u2003", "")
    content = content.replace("（求月票）", "")
    content = content.replace("（求收藏）", "")
    content = content.replace("\n\t", "")
    content = content.replace("\n", "")
    content = content.replace("            ", "")
    
    # 检查是否包含特定结束语句
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
    """
    读取一本小说的主函数
    
    参数:
    bookTitle - 书名
    url - 起始URL
    nextPagePre - 下一页URL前缀
    mode - 模式（complete完整模式或add追加模式）
    startSection - 起始章节索引
    """
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
                # 获取第一章内容
                title, contents, next_url = await catchNovel(playwright, nextPagePre, url)
                while(1):
                    # 处理标题
                    if len(title) > 0:
                        title = handle_title(title, index, bookTitle, oldTitle)
                        if len(title) > 0:
                            print(title)
                            oldTitle = title
                            index = index + 1
                            f.write(title)
                            f.write("\r\n") 

                    # 处理内容
                    contentList = contents.split("\n")
                    for content in contentList:
                        content = handle_content(content)
                        if len(content) == 0:
                            continue
                        f.write(content)
                        f.write("\r\n") 

                    # 延时后获取下一章
                    time.sleep(0.3)
                    title, contents, next_url = await catchNovel(playwright, nextPagePre, next_url)
            except Exception as e:
                print(e)
                f.close() 

# 小说列表配置
novelList=[
{
    "url":"https://m.paozw.org/biquge/376375/100890856.html",  # 小说起始URL
    "bookTitle":"混在墨西哥当警察",  # 书名
    "nextPagePreUrl":"https://m.paozw.org",  # 下一页URL前缀
    "mode":"new",  # 模式
    "sectionIdx":1  # 起始章节索引
}
]
# driver = webdriver.Chrome()

# 遍历小说列表并抓取
for novel in novelList:
     asyncio.run(readOneNovel(bookTitle=novel["bookTitle"], 
                              url=novel["url"], 
                              nextPagePre = novel["nextPagePreUrl"], 
                              mode=novel["mode"],
                              startSection=novel["sectionIdx"]))
