from django.contrib import admin
from django.urls import path, include
from wifimap.views import WifiNodeViewSet
from location.views import DeviceLocationViewSet, UserLocation
from destination.views import ChosenDestinationViewSet
from networks.views import NetworksViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('wifinodes', WifiNodeViewSet, basename='wifinodes')
router.register('devicel', DeviceLocationViewSet, basename='devicel')
router.register('chosendest', ChosenDestinationViewSet, basename='chosendest')
router.register('networks', NetworksViewSet, basename='networks')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('devicel/<int:device_id>/user_location', UserLocation.as_view()),
]
