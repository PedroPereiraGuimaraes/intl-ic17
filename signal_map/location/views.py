from rest_framework import viewsets, views
from .models import DeviceLocation
from .serializer import DeviceLocationSerializer
from rest_framework.response import Response
from networks.models import Networks

class DeviceLocationViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceLocationSerializer
    queryset = DeviceLocation.objects.all()

def triangulacao(x1, y1, distancia1, x2, y2, distancia2, x3, y3, distancia3):
    raio1 = distancia1
    raio2 = distancia2
    raio3 = distancia3

    ##Fazendo os calculos da triangulação por simplificação
    a = 2 * (-x1 + x2)
    b = 2 * (-y1 + y2)
    c = (raio1 ** 2) - (raio2 ** 2) - (x1 ** 2) + (x2 ** 2) - (y1 ** 2) + (y2 ** 2)
    d = 2 * (-x2 + x3)
    e = 2 * (-y2 + y3)
    f = (raio2 ** 2) - (raio3 ** 2) - (x2 ** 2) + (x3 ** 2) - (y2 ** 2) + (y3 ** 2)

    x = 10000
    y = 10000

    ##Calculando as coordenadas de x e y do dispositivo
    if ((e * a) - (b * d)) == 0 and ((b * d) - (a * e)) == 0:
        x = 0
        y = 0
    elif((e*a) - (b*d)) == 0:
        y = ((c * d) - (a * f)) / ((b * d) - (a * e))
        x=0
    elif((b * d) - (a * e)) == 0:
        x = ((c * e) - (f * b)) / ((e * a) - (b * d))
        y = 0
    else:
        x = ((c * e) - (f * b)) / ((e * a) - (b * d))
        y = ((c * d) - (a * f)) / ((b * d) - (a * e))

    return x, y

class UserLocation(views.APIView):
    def get(self, request, *args, **kwargs):
        device_id = self.kwargs['device_id']
        # Obtém as três redes mais próximas
        nearest_networks = DeviceLocation.objects.filter(device_id=device_id).order_by('distance')[:3]
        network_coords_dict = []
        
        for nearest_network in nearest_networks:
            network_x = Networks.objects.filter(bssid=nearest_network.bssid).values_list('x_coord', flat=True)
            network_y = Networks.objects.filter(bssid=nearest_network.bssid).values_list('y_coord', flat=True)
            network_coords_dict.append({'bssid': nearest_network.bssid, 'x': network_x[0], 'y': network_y[0], 'distance': nearest_network.distance})
        
        if len(network_coords_dict) == 3:
            x1 = network_coords_dict[0]['x']
            y1 = network_coords_dict[0]['y']
            distancia1 = nearest_networks[0].distance
            x2 = network_coords_dict[1]['x']
            y2 = network_coords_dict[1]['y']
            distancia2 = nearest_networks[1].distance
            x3 = network_coords_dict[2]['x']
            y3 = network_coords_dict[2]['y']
            distancia3 = nearest_networks[2].distance
            x, y = triangulacao(x1, y1, distancia1, x2, y2, distancia2, x3, y3, distancia3)
            return Response({
                'used networks': network_coords_dict,
                'x': x,
                'y': y
            })