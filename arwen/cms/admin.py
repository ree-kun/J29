from django.contrib import admin
from cms.models import BusinessDate
from cms.models import StockExchange
from cms.models import Brand
from cms.models import DailyPrice

admin.site.register(BusinessDate)
admin.site.register(StockExchange)
admin.site.register(Brand)
admin.site.register(DailyPrice)
