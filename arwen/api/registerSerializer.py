from datetime import datetime, date
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from cms.models import BusinessDate
from cms.models import Brand
from cms.models import DailyPrice
from cms.models import StockExchange


class RegisterMetaInfoSerializer(serializers.ModelSerializer):
    date = serializers.CharField(min_length=10, max_length=10)
    class Meta:
        model = BusinessDate
        fields = ('date',)

    def create(self, validated_data):
        date = datetime.strptime(validated_data['date'], '%Y-%m-%d').date()
        businessDate = BusinessDate.objects.filter(date=date)
        if (not businessDate.exists()):
            validated_data['date'] = date
            return super().create(validated_data)
        else:
            return businessDate[0]

class RegisterSerializer(serializers.ModelSerializer):
    stockExchange = serializers.CharField(max_length=250)
    openingPrice = serializers.FloatField()
    highPrice = serializers.FloatField()
    lowPrice = serializers.FloatField()
    closingPrice = serializers.FloatField()
    class Meta:
        model = Brand
        fields = ('brandCode', 'stockExchange', 'name',
                'openingPrice', 'highPrice', 'lowPrice', 'closingPrice')

    def __init__(self, *args, **kwargs):
        self.businessDate = kwargs.pop('businessDate', '')
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        # 証券取引所の登録
        name = validated_data['stockExchange']
        stockExchange = StockExchange.objects.filter(name=name)

        if (not stockExchange.exists()):
            stockExchange = StockExchange.objects.create(name=name, code='X')
        else:
            stockExchange = stockExchange[0]

        # 銘柄の登録
        new_brand = {'brandCode': validated_data['brandCode'], 'stockExchange': stockExchange}
        brand = Brand.objects.filter(**new_brand)

        if (not brand.exists()):
            new_brand['name'] = validated_data['name']
            brand = Brand.objects.create(**new_brand)
        else:
            brand = brand[0]

        # 日足の登録
        new_dailyPrice = {'brand': brand, 'businessDate': self.businessDate}
        dailyPrice = DailyPrice.objects.filter(**new_dailyPrice)

        if (not dailyPrice.exists()):
            new_dailyPrice['openingPrice'] = validated_data['openingPrice']
            new_dailyPrice['highPrice'] = validated_data['highPrice']
            new_dailyPrice['lowPrice'] = validated_data['lowPrice']
            new_dailyPrice['closingPrice'] = validated_data['closingPrice']
            dailyPrice = DailyPrice.objects.create(**new_dailyPrice)
        else:
            dailyPrice = dailyPrice[0]

        return dailyPrice
