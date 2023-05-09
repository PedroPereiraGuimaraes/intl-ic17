from django.db import models


class DeviceLocation(models.Model):
    device_id = models.CharField(max_length=32)
    bssid = models.CharField(max_length=17)
    rssi = models.FloatField()
    distance = models.FloatField(null=True)
    
    def calculate_distance(self, rssi):
        #rssi per meter
        a = -40
        # rssi - rssi/meter divided by pathLoss
        w = (rssi-a)/-20
        #log distance
        distance = 10**w
        
        return distance

    def save(self, *args, **kwargs):
        self.distance = self.calculate_distance(self.rssi)
        super().save(*args, **kwargs)