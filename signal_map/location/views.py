from rest_framework import viewsets
from .models import DeviceLocation
from .serializer import DeviceLocationSerializer

class DeviceLocationViewSet(viewsets.ModelViewSet):
    queryset = DeviceLocation.objects.all()
    serializer_class = DeviceLocationSerializer
    
#criar uma nova rota pra poder retornar o caminho do ponto para o dispositivo com base no local escolhido, mas talvez fazer esse calculo
#usando latitudes e longitudes seja mais facil, o dispositivo envia a latitude e longitude e o servidor retorna o caminho para o celular
