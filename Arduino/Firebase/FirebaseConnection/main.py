import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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

local = input("Local:")
ref = db.reference(f'/training/{local}')
data = ref.get()

redes = []
for mac, info in data.items():
    rssi = info.get('rssi')
    if rssi is not None:
        redes.append({'mac': info['mac'], 'rssi': rssi})

redes.sort(key=lambda x: x['rssi'], reverse=True)

for rede in redes[:5]:
    print(f"MAC: {rede['mac']}")
    print(f"RSSI: {rede['rssi']}")
    print(f"DISTANCE: {round(rssiParaDistancia(rede['rssi']),2)} metros")
    print()



