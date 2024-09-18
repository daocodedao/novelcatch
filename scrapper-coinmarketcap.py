import requests
from requests import Session
import json


class coinMarketCap:
    def newsParse(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
        # x = input("Enter name of the cryptocurrency")
        # 币的名称，可以多来几个
        x = "bitcoin,ethereum"
        parameters = {
            'slug': x,
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '904da0b1-0e09-488a-ab1b-152351674dec'
        }
        session = Session()
        session.headers.update(headers)
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        a = data['data']
        id = list(a.keys())[0]
        for x in range(1, 6):
            url1 = 'https://api.coinmarketcap.com/content/v3/news?coins=' + id + '&page=' + str(x) + '&size=5'

            coin_html = requests.get(url1).json()
            titles = []
            subtitles = []
            num = 1 * ((x - 1) * 5 + 1)
            for coin in coin_html['data']:
                print("Article number " + str(num))
                titles.append(coin['meta']['title'])
                print(coin['meta']['title'])
                subtitles.append(coin['meta']['subtitle'])
                print(coin['meta']['subtitle'])
                num = num + 1
            num += 5

coinMarketCap.newsParse(1)