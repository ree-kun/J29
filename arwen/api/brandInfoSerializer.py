from datetime import datetime, date, timedelta
import numpy
import urllib.request, json

from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from cms.models import Brand
from cms.models import DailyPrice
from .serializer import BrandSerializer, DailyPriceSerializer

# 株価情報取得サイトのURL
url = "https://ryoito.shop/detail/"

class BrandInfoSerializer(serializers.ModelSerializer):
    date = SerializerMethodField()
    brand = SerializerMethodField()
    dailyPrices = SerializerMethodField()
    class Meta:
        model = Brand
        fields = ('date', 'brand', 'dailyPrices')

    def __init__(self, *args, **kwargs):
        def get_base_date():
            today = date.today()
            baseDate = (
                today if not self.query_parameters.get('date', '')
                else datetime.strptime(
                    self.query_parameters.get('date'), '%Y%m%d').date())
            return baseDate

        self.query_parameters = kwargs['context']['request'].GET
        self.baseDate = get_base_date()
        self.date = self.baseDate - timedelta(days=365)
        self.options = (
            1 if not self.query_parameters.get('options')
            else int(self.query_parameters.get('options', 1))
        )
        super(BrandInfoSerializer, self).__init__(*args, **kwargs)

    def get_date(self, obj):
        return self.date.strftime('%Y%m%d')

    def get_brand(self, obj):
        brand = BrandSerializer(obj).data
        with urllib.request.urlopen(url + "?" + obj.brandCode + "+" + obj.stockExchange.code) as response:
                response_body = response.read().decode("utf-8")
                brand['detail'] = json.loads(response_body)

        return brand

    def get_dailyPrices(self, obj):
        # 移動平均線
        def add_movingAverageLine(base, dailyPrices, term, key):
            closingPrices = [dailyPrice.get('closingPrice') for dailyPrice in dailyPrices]
            movingAverages = [numpy.average(numpy.array(closingPrices[i:i + term]))
                    for i, dailyPriceAt in enumerate(dailyPrices[term - 1:])]

            for i, dailyPrice in enumerate(dailyPrices[term - 1:]):
                base[i + term - 1][key] = movingAverages[i]

        '''
            基点日時点の株価微分
            
            基点日と、その前後１日を含めた計３日間のデータで２次方程式を求め、その微分を返す。
                yi = axi^2 + bxi + c    (i = -1, 0, 1)

            i = 0 で (x0, y0) = (0, 0) とすると、c = 0である。
                yi = axi^2 + bxi        (i = -1, 1)
            の連立方程式を解き、その解a, bが求まると、
            ２次方程式の微分は
                y' = 2ax + b
            基点日時点(x0 = 0)では、y' = bである。
            ここでは、x(-1) = -1, x = 1として計算している。
        '''
        def add_priceDerivativeLine(base, dailyPrices, key):
            averagePrices = [dailyPrice.get('tradingvalue') / dailyPrice.get('tradeVolume') for dailyPrice in dailyPrices]
            # AX = Bとして計算
            A = numpy.array([[1, -1], [1, 1]])
            Bs = [numpy.array([averagePrices[i] - averagePrices[i + 1], averagePrices[i + 2] - averagePrices[i + 1]])
                    for i, dailyPriceAt in enumerate(averagePrices[1:-1])]

            for i, B in enumerate(Bs):
                X = numpy.linalg.solve(A, B)
                base[i + 1][key] = X[1]

        # MACD
        def add_MacdLine(base, dailyPrices, shortTerm, longTerm, averageTerm, key):
            closingPrices = numpy.array([dailyPrice.get('closingPrice') for dailyPrice in dailyPrices])
            macds = list()
            # 初日は単純移動平均とする
            shortEMA = numpy.average(closingPrices[longTerm - shortTerm:longTerm])
            longEMA = numpy.average(closingPrices[:longTerm])
            macd = shortEMA - longEMA
            base[longTerm - 1][key] = {'macd': macd}
            macds.append(macd)

            shortEMAConst = 2 / (shortTerm + 1)
            longEMAConst = 2 / (longTerm + 1)

            for i in range(len(dailyPrices) - longTerm):
                shortEMA += shortEMAConst * (closingPrices[i + longTerm] - shortEMA)
                longEMA += longEMAConst * (closingPrices[i + longTerm] - longEMA)
                macd = shortEMA - longEMA
                base[i + longTerm][key] = {'macd': macd}
                macds.append(macd)

            for i in range(len(macds) - averageTerm + 1):
                signal = numpy.average(numpy.array(macds[i:i + averageTerm]))
                base[i + longTerm + averageTerm - 2][key]['signal'] = signal

        # RSI
        def add_RsiLine(base, dailyPrices, term, key):
            closingPrices = numpy.array([dailyPrice.get('closingPrice') for dailyPrice in dailyPrices])
            diffPrices = closingPrices[1:] - closingPrices[0:-1]

            for i in range(len(dailyPrices) - term):
                termDiffPrices = diffPrices[i:i + term]
                plusTotal = termDiffPrices[termDiffPrices > 0].sum()
                minusTotal = termDiffPrices[termDiffPrices < 0].sum()
                base[i + term][key] = plusTotal / (plusTotal - minusTotal)


        dateRange = {'businessDate__date__gte': self.date,
                'businessDate__date__lte': self.baseDate}
        try:
            dailyPrices = DailyPriceSerializer(
                DailyPrice.objects.filter(
                    brand=obj.id, **dateRange),
                many=True).data

            units = dailyPrices
            options = self.options
            if not (options >> 0) & True:
                units = [{} for i in range(len(dailyPrices))]
            if (options >> 1) & True:
                add_movingAverageLine(units, dailyPrices, 5, 'option1')
            if (options >> 2) & True:
                add_movingAverageLine(units, dailyPrices, 10, 'option2')
            if (options >> 3) & True:
                add_movingAverageLine(units, dailyPrices, 15, 'option3')
            if (options >> 4) & True:
                add_priceDerivativeLine(units, dailyPrices, 'option4')
            if (options >> 5) & True:
                add_MacdLine(units, dailyPrices, 12, 26, 9, 'option5')
            if (options >> 6) & True:
                add_RsiLine(units, dailyPrices, 14, 'option6')

            return units
        except:
            dailyPrices = None
            return dailyPrices
