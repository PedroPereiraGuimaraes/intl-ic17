from rest_framework import serializers
from .models import WifiNode, UniqueNodeName

class WifiNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WifiNode
        fields = '__all__'

class UniqueNodeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniqueNodeName
        fields = '__all__'