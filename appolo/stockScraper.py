import sys, json
import urllib.request, urllib.parse
from time import sleep
from bs4 import BeautifulSoup


def getMetaInfo(soup):
    # ヘッダ情報
    header = soup.find("div", class_="base_box_desc").p.text
    date = header[-19:-9]

    return {'date': date}

def getStockInfo(soup):
    # 銘柄毎の株価情報
    stockPrices = soup.find("div", class_="data_contents").tbody.find_all("tr")

    stockInfo = list()

    # 要素の文字列を取得する
    for stockPrice in stockPrices:
        brandCodeAndName = stockPrice.a.string
        details = stockPrice.find_all("td")[1:]
        info = dict()
        info["brandCode"] = brandCodeAndName[:4]
        info["name"] = brandCodeAndName[5:]
        info["stockExchange"] = details[0].text
        info["openingPrice"] = float(details[1].text)
        info["highPrice"] = float(details[2].text)
        info["lowPrice"] = float(details[3].text)
        info["closingPrice"] = float(details[4].text)
        stockInfo.append(info)

    return stockInfo

def registStockInfo(stockInfo):
    url = 'https://www.ryoito.shop/api/register/'
    method = 'POST'
    headers = {'Content-Type' : 'application/json'}
    json_data = json.dumps(stockInfo).encode('utf-8')
    request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        if not len(response_body)==0:
            print(response_body)

args = sys.argv

# 株価情報サイトのURL
url = "https://kabuoji3.com/stock/"

if len(args) == 1:
    # クエリパラメータがない場合
    # URLにアクセスしてhtmlを取得

    html = urllib.request.urlopen(url)
    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")
    # ページ番号の一覧を取得
    pageNumbers = soup.find("ul", class_="pager").find_all("a")
    print([pageNumber.get("href")[6:] for pageNumber in pageNumbers])

else:
    # クエリパラメータがある場合
    # 株価情報を登録

    pageNumber = args[1]
    html = urllib.request.urlopen(url + '?page=' + pageNumber)
    soup = BeautifulSoup(html, "html.parser")
    # メタ情報を取得
    metaInfo = getMetaInfo(soup)
    # 株価情報を取得
    stockInfo = getStockInfo(soup)
    # 株価情報を保存
    registStockInfo({'metaInfo': metaInfo, 'stockInfo': stockInfo})
