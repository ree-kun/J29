from django.http import HttpResponse
from rest_framework import viewsets

from cms.models import Brand, StockExchange
from .serializer import DailyPriceSerializer
from .registerSerializer import RegisterMetaInfoSerializer, RegisterSerializer


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()

    def create(self, request):
        serializer = RegisterMetaInfoSerializer(data=request.data['metaInfo'])
        if not serializer.is_valid():
            return HttpResponse(serializer.errors)
        else:
            result = serializer.save()

        serializer = RegisterSerializer(data=request.data['stockInfo'], many=True, businessDate=result)
        if not serializer.is_valid():
            return HttpResponse(serializer.errors)
        else:
            result = serializer.save()
        return HttpResponse('')

class RegisterInitViewSet(RegisterViewSet):
    def create(self, request):
        data = request.data
        brand = Brand.objects.get(id=data['brand']['id'])
        stockExchange = brand.stockExchange

        new_dailyPrice_list = list()
        for pricesAndDate in data['prices']:
            # 営業日の登録
            serializer = RegisterMetaInfoSerializer(data={'date': pricesAndDate['businessDate']})
            if not serializer.is_valid():
                return HttpResponse(serializer.errors)
            else:
                result = serializer.save()

            # 日足データ登録の下準備
            dailyPrice = pricesAndDate.copy()
            dailyPrice['brand'] = brand.id
            dailyPrice['businessDate'] = result.id

            new_dailyPrice_list.append(dailyPrice)


        # 日足データの登録
        serializer = DailyPriceSerializer(data=new_dailyPrice_list, many=True)
        if not serializer.is_valid():
            return HttpResponse(serializer.errors)
        else:
            result = serializer.save()
        return HttpResponse('')
