from django.db import models
from wifimap.models import UniqueNodeName

class ChosenDestination(models.Model):
    device_id = models.CharField(max_length=32) #device id that is used to identify the user
    node_name = models.ForeignKey(UniqueNodeName, on_delete=models.CASCADE, default=1)