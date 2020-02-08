from django.db.models import Max
from rest_framework import viewsets

from cms.models import DailyPrice, BusinessDate
from .registedDailyPriceSerializer import RegistedDailyPriceSerializer


class RegistedDailyPriceViewSet(viewsets.ModelViewSet):
    serializer_class = RegistedDailyPriceSerializer

    def get_queryset(self):
        lastDateSerialNumber = BusinessDate.objects.aggregate(serialNumber=Max('serialNumber'))
        queryset = DailyPrice.objects.filter(businessDate__serialNumber=lastDateSerialNumber['serialNumber'])
        return queryset
