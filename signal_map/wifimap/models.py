from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class WifiNode(models.Model):
    node_name = models.CharField(max_length=50, null=False, default='')
    bssid = models.CharField(max_length=17) #mac address
    rssi = models.FloatField() #signal strength
    #use result from calculate_distance
    distance = models.FloatField(null=True)
    
    def calculate_distance(self, rssi):
        #rssi per meter
        a = -40
        # rssi - rssi/meter divided by pathLoss
        w = (rssi-a)/-20
        #log distance
        distance = 10**w
        
        return distance

    def __str__(self):
        return self.node_name

    def save(self, *args, **kwargs):
        self.distance = self.calculate_distance(self.rssi)
        super().save(*args, **kwargs)


class UniqueNodeName(models.Model):
    node_name  = models.CharField(max_length=50, unique=True, null=False, default='') #location where wifi node is placed
    
@receiver(post_save, sender=WifiNode)
def create_unique_node_name(sender, instance, created, **kwargs):
    if created:
        try:
            unique_name = UniqueNodeName.objects.get(node_name=instance.node_name)
        except UniqueNodeName.DoesNotExist:
            unique_name = UniqueNodeName.objects.create(node_name=instance.node_name)

        instance.unique_node_name = unique_name
        instance.save()
