from django.db import models

class Networks(models.Model):
    bssid = models.CharField(max_length=17)
    x_coord = models.FloatField()
    y_coord = models.FloatField()

    def __str__(self):
        self.bssid
        
