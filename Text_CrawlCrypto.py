
import time
from selenium import webdriver
from lxml import etree

def catchDetail(url):
    try:
        driver.get(url)

        while driver.execute_script("return document.readyState") != "complete":
            time.sleep(1)

        text = driver.page_source  

        html = etree.HTML(text)
        content = html.xpath('//*[@class="is-style-lead"]/text()')[0]
    except Exception as e:
        print(e)
        content = ""

    return content


def catchOneNews(url):
    driver.get(url)

    while driver.execute_script("return document.readyState") != "complete":
        time.sleep(1)

    text = driver.page_source  

    html = etree.HTML(text)

    title = html.xpath('//*[@class="post-loop__link"]/text()')
    datetime = html.xpath('//*[@class="post-loop__date"]/@datetime')
    next_url = html.xpath('//*[@class="post-loop__link"]/@href')


    return title, datetime, next_url


def catchNews(url):
    while(True):

        try:
            titles, datetimes, detailUrls = catchOneNews(url)

            titlesLen = len(titles)
            datetimesLen = len(datetimes)
            detailUrlsLen = len(detailUrls)
            print(f"title len:{titlesLen}")
            print(f"datetime len:{datetimesLen}")
            print(f"next_url len:{detailUrlsLen}")

            if titlesLen != datetimesLen or titlesLen != detailUrlsLen or datetimesLen != detailUrlsLen:
                print("len different")
            else:
                for i in range(titlesLen):
                    title = titles[i]
                    title = title.replace("\n", "")
                    title = title.replace("                    ", "")

                    detailUrl = detailUrls[i]
                    content = catchDetail(detailUrl)
                    content = content.replace("\xa0", "")

                    
                    print(f"title:{title}")
                    print(f"datetime:{datetimes[i]}")
                    print(f"detail_url:{detailUrl}")
                    print(f"content:{content}")
                    print("----------------------------------------------------")
                    time.sleep(0.3)
            
            print("sleep 30s")
            time.sleep(30)

        except Exception as e:
            print(e)


driver = webdriver.Chrome()
url = "https://crypto.news/news/"
catchNews(url)

