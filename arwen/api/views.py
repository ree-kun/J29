import django_filters
from rest_framework import viewsets

from cms.models import Brand
from cms.models import DailyPrice
from .serializer import BrandSerializer
from .serializer import DailyPriceSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_fields = ('brandCode',)

class DailyPriceViewSet(viewsets.ModelViewSet):
    queryset = DailyPrice.objects.all()
    serializer_class = DailyPriceSerializer
    filter_fields = ('brand',)
