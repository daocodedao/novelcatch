import requests
from lxml import etree
import sys
import time


headers = {
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
}


def catchDetail(url):
    try:
        resp = requests.get(url, headers)
        html = etree.HTML(resp.content)
        content = html.xpath('//*[@class="is-style-lead"]/text()')[0]
    except Exception as e:
        print(e)
        content = ""

    return content

def catchOneNews(url):
    # 使用get方法请求网页
    resp = requests.get(url, headers)

    # 将网页内容按utf-8规范解码为文本形式
    # text = resp.content.decode('GB2312')

    # 将文本内容创建为可解析元素
    html = etree.HTML(resp.content)

    # /html/body/div[1]/div[3]/div/div[1]/h1/text()
    # //*[@id="m-article-title"]/text()
    title = html.xpath('//*[@class="sc-4984dd93-0 sc-ef20e69b-0 fCIfpP title"]/text()')
    content = html.xpath('//*[@class="sc-4984dd93-0 sc-ef20e69b-0 ePvyhe description"]/text()')
    datetime = html.xpath('//*[@class="sc-aef7b723-0 LCOyB date-info"]/text()')
    # next_url = html.xpath('//*[@class="post-loop__link"]/@href')


    # print(next_url_element)
    return title, datetime, content




def catchNews(url):
    while(True):
        try:
            titles, datetimes, contents = catchOneNews(url)
            
            titlesLen = len(titles)
            datetimesLen = len(datetimes)
            contentsLen = len(contents)
            print(f"title len:{titlesLen}")
            print(f"datetime len:{datetimesLen}")
            print(f"next_url len:{contentsLen}")

            if titlesLen != datetimesLen or titlesLen != contentsLen or datetimesLen != contentsLen:
                print("len different")
            else:
                for i in range(titlesLen):
                    title = titles[i]
                    title = title.replace("\n", "")
                    title = title.replace("                    ", "")

                    content = contents[i]
                    # content = catchDetail(content)
                    # content = content.replace("\xa0", "")

                    
                    print(f"title:{title}")
                    print(f"datetime:{datetimes[i]}")
                    print(f"content:{content}")
                    print(f"content:{content}")
                    print("----------------------------------------------------")
                    time.sleep(0.3)
            
            print("sleep 30s")
            time.sleep(30)

        except Exception as e:
            print(e)

        
url = "https://coinmarketcap.com/community/articles/browse/?sort=-publishedOn&page=1&category="
catchNews(url)

