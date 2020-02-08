from django.db import models

# 営業日
class BusinessDate(models.Model):
    class Meta:
        verbose_name = '営業日'
        verbose_name_plural = '営業日'

    def get_next():
        return BusinessDate.objects.count() + 1
 
    serialNumber = models.IntegerField(default=get_next)
    date = models.DateField('日付', unique=True)

    def __str__(self):
        return self.date.strftime('%Y/%m/%d') + "(" + str(self.serialNumber) + ")"

# 証券取引所
class StockExchange(models.Model):
    class Meta:
        verbose_name = '証券取引所'
        verbose_name_plural = '証券取引所'

    TOKYO = 'T'
    NAGOYA = 'N'
    FUKUOKA = 'F'
    SAPPORO = 'S'
    UNKNOWN = 'X'
    STOCK_EXCHANGE = (
            (TOKYO, '東京'),
            (NAGOYA, '名古屋'),
            (FUKUOKA, '福岡'),
            (SAPPORO, '札幌'),
            (UNKNOWN, '未定義'),
    )
    name = models.CharField('市場名', unique=True, max_length=250)
    code = models.CharField('市場コード', choices=STOCK_EXCHANGE, max_length=1)

    def __str__(self):
        return self.name + "(" + self.code + ")"

# 銘柄
class Brand(models.Model):
    class Meta:
        verbose_name = '銘柄'
        verbose_name_plural = '銘柄'
        unique_together = (('brandCode', 'stockExchange'),)

    TOKYO = 'T'
    NAGOYA = 'N'
    FUKUOKA = 'F'
    SAPPORO = 'S'
    STOCK_EXCHANGE = (
            (TOKYO, '東京'),
            (NAGOYA, '名古屋'),
            (FUKUOKA, '福岡'),
            (SAPPORO, '札幌'),
    )
    brandCode = models.CharField('銘柄コード', max_length=4)
    stockExchange = models.ForeignKey(StockExchange, verbose_name='市場', related_name='stockExchange', on_delete=models.CASCADE)
    name = models.CharField('銘柄名', max_length=250)

    def __str__(self):
        return self.brandCode + "(" + self.stockExchange.code + "): " + self.name

# 日足
class DailyPrice(models.Model):
    class Meta:
        verbose_name = '日足'
        verbose_name_plural = '日足'
        unique_together = (('brand', 'businessDate'),)

    brand = models.ForeignKey(Brand, verbose_name='銘柄', related_name='brand', on_delete=models.CASCADE)
    businessDate = models.ForeignKey(BusinessDate, verbose_name='日付', related_name='businessDate', on_delete=models.CASCADE)
    lowPrice = models.FloatField('安値')
    openingPrice = models.FloatField('始値')
    closingPrice = models.FloatField('終値')
    highPrice = models.FloatField('高値')

    def __str__(self):
        return self.brand.__str__() + ": " + self.businessDate.date.strftime('%Y/%m/%d')
