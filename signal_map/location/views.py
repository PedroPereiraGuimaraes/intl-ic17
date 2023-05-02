from rest_framework import viewsets, generics
from .models import DeviceLocation
from .serializer import DeviceLocationSerializer
from rest_framework.response import Response
from wifimap.serializer import WifiNodeSerializer
from wifimap.models import WifiNode
class DeviceLocationViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceLocationSerializer
    queryset = DeviceLocation.objects.all()
    
class NearestNetworks(generics.GenericAPIView):
    serializer_class = DeviceLocationSerializer

    def get_queryset(self):
        device_id = self.kwargs['device_id']
        queryset = DeviceLocation.objects.filter(device_id=device_id).order_by('distance')[:3]
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'results': serializer.data
        }
        return Response(data)

class NearestWifiNodes(generics.ListAPIView):
    serializer_class = WifiNodeSerializer

    def get_queryset(self):
        # Obter os SSIDs das três redes mais próximas
        device_id = self.kwargs['device_id']
        networks = DeviceLocation.objects.filter(device_id=device_id).order_by('distance')[:3]
        ssids = [network.ssid for network in networks]

        # Filtrar os nós Wi-Fi com base nos SSIDs das redes
        queryset = WifiNode.objects.filter(ssid__in=ssids)

        return queryset