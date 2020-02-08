import json, re
import urllib.request
from time import sleep
from bs4 import BeautifulSoup


# 株価情報サイトのURL
url = "https://kabuoji3.com/stock/"

def getPriceInfo(brand):
    brandCode = brand['brandCode']

    # URLにアクセスしてhtmlを取得
    html = urllib.request.urlopen(url + brandCode + '/')
    html = html.read().decode('utf-8')
    # </tbody>が不要な箇所にも混ざっているため、正規表現で<tbody>を追加するよう加工
    pattern = '(?<=/tbody>\s)(?=\s+<tr>)'
    html = re.sub(pattern, '\n<tbody>', html)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")
    # 日付毎の株価情報
    pricesAndDates = soup.find("div", class_="data_contents").find_all('tbody')

    priceInfo = list()

    # 要素の文字列を取得する
    for pricesAndDate in reversed(pricesAndDates):
        details = pricesAndDate.find_all("td")
        info = dict()
        info['businessDate'] = details[0].text
        info["openingPrice"] = float(details[1].text)
        info["highPrice"] = float(details[2].text)
        info["lowPrice"] = float(details[3].text)
        info["closingPrice"] = float(details[4].text)
        priceInfo.append(info)

    return priceInfo

def registPriceInfo(priceInfo):
    url = 'https://www.ryoito.shop/api/registerInit/'
    method = 'POST'
    headers = {'Content-Type' : 'application/json'}
    json_data = json.dumps(priceInfo).encode('utf-8')
    request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        if not len(response_body)==0:
            print(response_body)

# 銘柄一覧取得API
urlAPI = 'https://www.ryoito.shop/api/brands/?format=json'
# URLにアクセス
response = urllib.request.urlopen(urlAPI)
# 銘柄一覧を取得
brands = json.load(response)
brand = brands[0]

# 株価情報を取得
priceInfo = getPriceInfo(brand)
registPriceInfo({'brand': brand, 'prices': priceInfo})

for brand in brands[1:]:
    sleep(2)
    priceInfo = getPriceInfo(brand)
    # 株価情報を保存
    registPriceInfo({'brand': brand, 'prices': priceInfo})
