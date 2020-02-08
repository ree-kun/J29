from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from cms.models import DailyPrice
from .serializer import BrandSerializer


class RegistedDailyPriceSerializer(serializers.ModelSerializer):
    brand = SerializerMethodField()
    date = serializers.DateField(source='businessDate.date')
    class Meta:
        model = DailyPrice
        fields = ('brand', 'date',
                  'lowPrice', 'openingPrice', 'closingPrice', 'highPrice')

    def get_brand(self, obj):
        return BrandSerializer(obj.brand).data
