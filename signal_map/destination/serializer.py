from rest_framework import serializers
from .models import ChosenDestination

class ChosenDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChosenDestination
        fields = '__all__'