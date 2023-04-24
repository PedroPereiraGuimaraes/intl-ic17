from django.contrib import admin
from django.urls import path, include
from wifimap.views import WifiNodeViewSet
from location.views import DeviceLocationViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('wifinodes', WifiNodeViewSet, basename='wifinodes')
router.register('devicel', DeviceLocationViewSet, basename='devicel')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
