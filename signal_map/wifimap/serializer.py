from rest_framework import serializers
from .models import WifiNode

class WifiNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WifiNode
        fields = '__all__'