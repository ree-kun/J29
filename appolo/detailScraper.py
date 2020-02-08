import json, sys, re
import urllib.request
from time import sleep
from bs4 import BeautifulSoup


def getDetailInfo(soup):
    # 詳細情報
    detailInfo = soup.find("div", class_="innerDate").find_all("dl")
    info = dict()
    info["prevClosingPrice"] = float(detailInfo[0].dd.strong.text)
    info["openingPrice"] = float(detailInfo[1].dd.strong.text)
    info["highPrice"] = float(detailInfo[2].dd.strong.text)
    info["lowPrice"] = float(detailInfo[3].dd.strong.text)
    info["tradeVolume"] = float(detailInfo[4].dd.strong.text)
    info["tradingvalue"] = float(detailInfo[5].dd.strong.text)
    valueRange = detailInfo[6].dd.strong.text.split('～')
    info["minValueRange"] = float(valueRange[0])
    info["maxValueRange"] = float(valueRange[1])

    return info

def getReferenceIndex(soup):
    # 銘柄毎の株価情報
    referenceIndex = soup.find("div", id="rfindex")
    if referenceIndex:
        # id=rfindex の参考指標がある場合、株式会社の銘柄と判断
        referenceIndex = referenceIndex.find_all("dl")

        # "(連) "が先頭に付いている項目があるため、削除するための正規表現
        pattern = '^.+?(?=\d)'

        info = dict()
        info["marketCapitalization"] = float(referenceIndex[0].dd.strong.text)
        info["commonSharesOutstanding"] = float(referenceIndex[1].dd.strong.text)
        info["dividendYield"] = float(referenceIndex[2].dd.strong.text)
        info["dividendPerShare"] = float(referenceIndex[3].dd.strong.a.text)
        info["priceEarningsRatio"] = float(re.sub(pattern, '', referenceIndex[4].dd.strong.text))
        info["priceBookvalueRatio"] = float(re.sub(pattern, '', referenceIndex[5].dd.strong.text))
        info["earningsPerShare"] = float(re.sub(pattern, '', referenceIndex[6].dd.strong.a.text))
        info["bookvaluePerShare"] = float(re.sub(pattern, '', referenceIndex[7].dd.strong.a.text))
        info["minPurchaseValue"] = float(referenceIndex[8].dd.strong.text)
        info["shareUnitNumber"] = float(referenceIndex[9].dd.strong.text)
        info["yearToDateHigh"] = float(referenceIndex[10].dd.strong.text)
        info["yearToDateLow"] = float(referenceIndex[11].dd.strong.text)

        return info
    else:
        # 上記以外の場合、投資信託の銘柄と判断
        referenceIndex = soup.find("div", class_="main2colR clearFix").find_all("dl")

        # "YYYY年m月d日"形式の日付を"YYYYmmdd"形式に変換するための正規表現
        pattern = '(?<=年|月)(?=\d(?:月|日))'

        info = dict()
        info["netAsset"] = float(referenceIndex[0].dd.strong.text)
        info["minPurchaseValue"] = float(referenceIndex[1].dd.strong.text)
        info["tradingUnit"] = float(referenceIndex[2].dd.strong.text)
        info["yearToDateHigh"] = float(referenceIndex[3].dd.strong.text)
        info["yearToDateLow"] = float(referenceIndex[4].dd.strong.text)
        info["managementCompany"] = referenceIndex[5].dd.strong.text
        info["investmentAsset"] = referenceIndex[6].dd.strong.text
        info["investmentArea"] = referenceIndex[7].dd.strong.text
        info["interlockTarget"] = referenceIndex[8].dd.strong.text
        info["accountingCount"] = int(referenceIndex[9].dd.strong.text)
        info["accountingMonth"] = int(referenceIndex[10].dd.strong.text)
        info["listedDate"] = re.sub('年|月|日', '', re.sub(pattern, '0', referenceIndex[11].dd.strong.text))
        info["custodianFee"] = float(referenceIndex[12].dd.strong.text[:-1])

        return info

args = sys.argv
if not len(args) == 3:
    # クエリパラメータが2つない場合は処理終了
    sys.exit(0)

# Yahoo financeのURL
url = "https://stocks.finance.yahoo.co.jp/stocks/detail/"
# URLにアクセスしてhtmlを取得
html = urllib.request.urlopen(url + "?code=" + args[1] + "." + args[2])
# 価格が3桁毎に","区切りになっているため削除
html = re.sub('(?<=\d),(?=\d)', '', html.read().decode('utf-8'))

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(html, "html.parser")

# 詳細情報を取得
detailInfo = getDetailInfo(soup)
# 参考指標を取得
referenceIndex = getReferenceIndex(soup)
print(json.dumps({'detailInfo': detailInfo, 'referenceIndex': referenceIndex}))
