from rest_framework import viewsets

from cms.models import Brand
from .brandInfoSerializer import BrandInfoSerializer


class BrandInfoViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandInfoSerializer
    filter_fields = ('brandCode',)
