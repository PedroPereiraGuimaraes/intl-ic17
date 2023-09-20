import math

def triangulacao(x1, y1, rssi1, x2, y2, rssi2, x3, y3, rssi3):

    raio1 = rssiParaDistancia(rssi1)
    raio2 = rssiParaDistancia(rssi2)
    raio3 = rssiParaDistancia(rssi3)

    a = 2 * (-x1 + x2)
    b = 2 * (-y1 + y2)
    c = (raio1 ** 2) - (raio2 ** 2) - (x1 ** 2) + (x2 ** 2) - (y1 ** 2) + (y2 ** 2)
    d = 2 * (-x2 + x3)
    e = 2 * (-y2 + y3)
    f = (raio2 ** 2) - (raio3 ** 2) - (x2 ** 2) + (x3 ** 2) - (y2 ** 2) + (y3 ** 2)

    x = 10000
    y = 10000

    if ((e * a) - (b * d)) == 0 & ((b * d) - (a * e)) == 0:
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

def rssiParaDistancia(rssi):
    a = -45
    w = (rssi - a) / -40
    distancia = 10 ** w

    return distancia

def distanciaParaRssi(distancia):
    rssi = -50 - 40*math.log(distancia,10)
    return rssi

def compararMac(redes, mac):
  for rede in redes:
    if rede["mac"] == mac:
      return rede["x"], rede["y"]
  return None