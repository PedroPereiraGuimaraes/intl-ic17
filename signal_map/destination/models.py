from django.db import models
from wifimap.models import WifiNode

class ChosenDestination(models.Model):
    device_id = models.CharField(max_length=32) #device id that is used to identify the user
    wifi_node = models.ForeignKey(WifiNode, on_delete=models.CASCADE, default=1)