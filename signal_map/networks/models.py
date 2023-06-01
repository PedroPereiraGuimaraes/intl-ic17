from django.db import models

class Networks(models.Model):
    node_name = models.ForeignKey('wifimap.UniqueNodeName', on_delete=models.CASCADE, default='')
    x_coord = models.FloatField()
    y_coord = models.FloatField()

        
