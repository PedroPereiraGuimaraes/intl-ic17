from rest_framework import viewsets
from .models import WifiNode, UniqueNodeName
from .serializer import WifiNodeSerializer, UniqueNodeNameSerializer

class WifiNodeViewSet(viewsets.ModelViewSet):
    queryset = WifiNode.objects.all()
    serializer_class = WifiNodeSerializer
    
class UniqueNodeNameViewSet(viewsets.ModelViewSet):
    queryset = UniqueNodeName.objects.all()
    serializer_class = UniqueNodeNameSerializer
