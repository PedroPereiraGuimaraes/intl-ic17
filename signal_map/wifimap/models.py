from django.db import models

class WifiNode(models.Model):
    measure_point = models.IntegerField()
    bssid = models.CharField(max_length=17) #mac address
    ssid = models.CharField(max_length=32) #network name
    rssi = models.IntegerField() #signal strength
    timestamp = models.DateTimeField(auto_now_add=True) #date and time
    #use result from calculate_distance
    distance = models.FloatField(null=True)
    
    def calculate_distance(self, rssi):
        #rssi per meter
        a = -50
        # rssi - rssi/meter divided by pathLoss
        w = (rssi-a)/-20
        #log distance
        distance = 10**w
        
        return distance

    def save(self, *args, **kwargs):
        self.distance = self.calculate_distance(self.rssi)
        super().save(*args, **kwargs)
