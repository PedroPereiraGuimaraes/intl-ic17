from django.contrib import admin
from django.urls import path, include
from wifimap.views import WifiNodeViewSet
from location.views import DeviceLocationViewSet, NearestNetworks, NearestWifiNodes
from destination.views import ChosenDestinationViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('wifinodes', WifiNodeViewSet, basename='wifinodes')
router.register('devicel', DeviceLocationViewSet, basename='devicel')
router.register('chosendest', ChosenDestinationViewSet, basename='chosendest')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('devicel/<int:device_id>/nearest_networks', NearestNetworks.as_view()),
    path('devicel/<int:device_id>/nearest_nodes', NearestWifiNodes.as_view()),
]
