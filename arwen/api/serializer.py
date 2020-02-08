from rest_framework import serializers

from cms.models import BusinessDate, StockExchange, Brand, DailyPrice


class BusinessDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDate
        fields = ('serialNumber', 'date')

class StockExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockExchange
        fields = ('name', 'code')

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'brandCode', 'stockExchange', 'name')

class DailyPriceSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source='businessDate.date')
    class Meta:
        model = DailyPrice
        fields = ('brand', 'date',
                  'lowPrice', 'openingPrice', 'closingPrice', 'highPrice')
