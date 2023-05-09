from rest_framework import viewsets
from .models import ChosenDestination
from .serializer import ChosenDestinationSerializer

class ChosenDestinationViewSet(viewsets.ModelViewSet):
    queryset = ChosenDestination.objects.all()
    serializer_class = ChosenDestinationSerializer