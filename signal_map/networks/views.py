from rest_framework import viewsets
from .models import Networks
from .serializer import NetworksSerializer

class NetworksViewSet(viewsets.ModelViewSet):
    queryset = Networks.objects.all()
    serializer_class = NetworksSerializer