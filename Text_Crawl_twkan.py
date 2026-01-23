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
        # 使用 Chromium 并添加更多参数绕过检测
        browser = await playwright.firefox.launch(
            headless=False,
            # executable_path="/Users/linzhiji/Library/Caches/ms-playwright/chromium-1155/chrome-mac/Chromium.app/Contents/MacOS/Chromium",
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-images',
                '--disable-javascript',  # 先禁用JS加载，然后在页面中启用
                '--no-first-run',
                '--no-service-autorun',
                '--password-store=basic',
                '--use-mock-keychain',
                '--disable-web-security',
                '--allow-running-insecure-content'
            ]
        )
        
        # 创建更真实的浏览器上下文
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='zh-CN,zh;q=0.9,en;q=0.8',
            timezone_id='Asia/Shanghai',
            extra_http_headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'upgrade-insecure-requests': '1',
            }
        )
        page = await context.new_page()
        
        # 添加脚本以绕过自动化检测
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // 修改插件属性
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // 修改 languages 属性
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en'],
            });
            
            // 修改 webgl 属性
            const originalWebgl = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function(...args) {
                const context = originalWebgl.apply(this, args);
                if (context && context.constructor.name === 'WebGLRenderingContext') {
                    Object.defineProperties(context, {
                        drawingBufferWidth: { get: () => 1920 },
                        drawingBufferHeight: { get: () => 1080 }
                    });
                }
                return context;
            };
        """)
    
    # 首先访问一个通用页面建立会话
    await page.goto("https://www.google.com")
    await page.wait_for_timeout(2000)
    
    # 然后访问目标网站
    await page.goto(url)
    
    # 检查是否出现 Cloudflare 验证
    try:
        # 等待可能的 Cloudflare 验证完成
        cloudflare_selector = 'div[class*="challenge"]'
        if await page.query_selector(cloudflare_selector) or 'Checking your browser' in await page.title():
            print("检测到 Cloudflare 验证，等待验证完成...")
            # 等待 Cloudflare 验证完成，最多等待 30 秒
            try:
                await page.wait_for_selector(cloudflare_selector, state='hidden', timeout=30000)
            except:
                # 如果等待超时，尝试模拟鼠标移动
                await page.mouse.move(100, 100)
                await page.mouse.move(200, 200)
                await page.wait_for_timeout(5000)
        
        # 等待页面完全加载
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(5000)
    except:
        pass
    for i in range(10):
        # 重试次数 = 10
        # errorCount = 0
        try:
            # //*[@id="sticky-parent"]/div[2]/div[3]
            # //*[@id="sticky-parent"]/div[2]/div[3]
            # titleNode = await page.query_selector('//*[@id="sticky-parent"]/div[2]/div[3]')
            titleNode = await page.query_selector('//*[@class="txtnav"]/h1')
            title = await titleNode.text_content()
            title = convert(title, 'zh-cn')
            contentNode = await page.query_selector('//*[@id="txtcontent0"]')
            contents = await contentNode.text_content()
            contents = convert(contents, 'zh-cn')

            # //*[@id="mm-5"]/div[2]/div/ul/li[2]/a
            nextNode = await page.query_selector('//*[@class="page1"]/a[4]')
            next_url = await nextNode.get_attribute("href")  #定义text变量接收a标签底下的href属性

            next_url = nextPagePre + next_url
            # errorCount = 0
            return title, contents, next_url
        except Exception as e:
            print(f"sleep 15s {e}")
            time.sleep(15)
            # time.sleep(random.uniform(0, 4))
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
    "url":"https://twkan.com/txt/77384/50597805",
    "bookTitle":"叫谁小鲜肉,我是天王",
    "nextPagePreUrl":"",  # 下一页URL前缀
    "mode":"add",  # 模式
    "sectionIdx":551  # 起始章节索引
}
]
# driver = webdriver.Chrome()

for novel in novelList:
     asyncio.run(readOneNovel(bookTitle=novel["bookTitle"], 
                              url=novel["url"], 
                              nextPagePre = novel["nextPagePreUrl"], 
                              mode=novel["mode"],
                              startSection=novel["sectionIdx"]))
