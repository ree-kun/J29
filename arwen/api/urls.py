from rest_framework import routers
from .views import BrandViewSet
from .views import DailyPriceViewSet
from .brandInfoViews import BrandInfoViewSet
from .registerViews import RegisterViewSet, RegisterInitViewSet
from .registedDailyPriceViews import RegistedDailyPriceViewSet

router = routers.DefaultRouter()
router.register('brands', BrandViewSet, basename='brands')
router.register('dailyPrice', DailyPriceViewSet, basename='dailyPrice')
router.register('brandInfo', BrandInfoViewSet, basename='brandInfo')
router.register('register', RegisterViewSet, basename='register')
router.register('registerInit', RegisterInitViewSet, basename='registerInit')
router.register('registedDailyPrice', RegistedDailyPriceViewSet, basename='registedDailyPrice')
