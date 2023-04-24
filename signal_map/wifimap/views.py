from rest_framework import viewsets
from .models import WifiNode
from .serializer import WifiNodeSerializer

class WifiNodeViewSet(viewsets.ModelViewSet):
    queryset = WifiNode.objects.all()
    serializer_class = WifiNodeSerializer
