from rest_framework import viewsets, views
from .models import DeviceLocation
from .serializer import DeviceLocationSerializer
from networks.models import Networks
from wifimap.models import WifiNode, UniqueNodeName
from rest_framework.response import Response
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
        
    def device_coords(self, device_id):
        nearest_networks = DeviceLocation.objects.filter(device_id=device_id).order_by('distance')[:3]
        nearest_nodes = []
        
        for network in nearest_networks:
            network_node = WifiNode.objects.filter(bssid=network.bssid).order_by('distance').first()

            device_network_distance = network.distance
            node_network_distance = network_node.distance
            device_node_distance = (device_network_distance * node_network_distance) / (device_network_distance**2)
            node_name = UniqueNodeName.objects.filter(node_name=network_node).first().id
            network_coords = Networks.objects.filter(node_name_id=node_name).first()
            x_node, y_node = network_coords.x_coord, network_coords.y_coord
                    
            print("network_node: " + str(network_node))
            print("network_node.bssid: " + str(network_node.bssid))
            print("device_node_distance: " + str(device_node_distance))
            print("node_name: " + str(node_name))
            print("x_node: " + str(x_node))
            print("y_node: " + str(y_node))
            
            data = {
                "network_node": network_node,
                "network_node.bssid": network_node.bssid,
                "device_node_distance": device_node_distance,
                "node_name": node_name,
                "x_node": x_node,
                "y_node": y_node
            }
            
            nearest_nodes.append(data)
        
        print("nearest_nodes: " + str(nearest_nodes))
        
        
        x1 = nearest_nodes[0]["x_node"]
        y1 = nearest_nodes[0]["y_node"]
        distancia1 = nearest_nodes[0]["device_node_distance"]
        x2 = nearest_nodes[1]["x_node"]
        y2 = nearest_nodes[1]["y_node"]
        distancia2 = nearest_nodes[1]["device_node_distance"]
        x3 = nearest_nodes[2]["x_node"]
        y3 = nearest_nodes[2]["y_node"]
        distancia3 = nearest_nodes[2]["device_node_distance"]
        
        x_device, y_device = triangulacao(x1, y1, distancia1, x2, y2, distancia2, x3, y3, distancia3)
        
        return x_device, y_device  
                        
        
    def get(self, request, *args, **kwargs):
        x_device, y_device = self.device_coords(self.kwargs['device_id'])
        
        return Response({
            "x_device": x_device,
            "y_device": y_device
            })