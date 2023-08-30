import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd

cred = credentials.Certificate("esp8266.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://esp8266-2dca6-default-rtdb.firebaseio.com/'
})

def rssiParaDistancia(rssi):
    # Rssi por um metro
    a = -45
    # Rssi - Rssi/metro dividido pelo PathLoss
    w = (rssi - a) / -40
    # Calculo do Log(distancia)
    distancia = 10 ** w

    return distancia

redes = []
cont = 1

while cont != "0":
    local = input("Local:")
    ref = db.reference(f'/training/{local}')
    data = ref.get()
    for mac, info in data.items():
        rssi = info.get('rssi')
        if rssi is not None:
            macseparado = info['mac'].split(':')
            macseparado = [int(digit, 16) for digit in macseparado]
            redes.append({'mac0':macseparado[0] ,'mac1':macseparado[1] ,'mac2':macseparado[2] ,'mac3':macseparado[3] ,'mac4':macseparado[4] ,'mac5':macseparado[5] , 'rssi': rssi, 'local': local})
    cont = input("0 pra sair 1 pra continuar\n")

redes.sort(key=lambda x: x['rssi'], reverse=True)
df = pd.DataFrame(redes)

df.to_csv('rede.csv', index=False, sep=';')
