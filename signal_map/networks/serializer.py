from rest_framework import serializers
from .models import Networks

class NetworksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Networks
        fields = '__all__'