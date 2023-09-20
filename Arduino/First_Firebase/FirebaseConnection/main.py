import firebase_admin
from triangulation import *
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd

cred = credentials.Certificate("esp8266.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://esp8266-2dca6-default-rtdb.firebaseio.com/'
})

redes = [
  {"mac": "20:58:69:0E:AA:38", "nome": "WLL-Inatel", "x": "0", "y": "1"},
  {"mac": "30:87:D9:02:FA:C8", "nome": "WLL-Inatel", "x": "0", "y": "1"},
  {"mac": "30:87:D9:02:FE:08", "nome": "WLL-Inatel", "x": "0", "y": "1"},
  {"mac": "B4:79:C8:05:B9:38", "nome": "WLL-Inatel", "x": "0", "y": "1"},
  {"mac": "B4:79:C8:05:B9:A8", "nome": "WLL-Inatel", "x": "0", "y": "1"},
  {"mac": "B4:79:C8:05:C2:38", "nome": "WLL-Inatel", "x": "0", "y": "1"},
  {"mac": "B4:79:C8:05:C2:78", "nome": "WLL-Inatel", "x": "0", "y": "1"},
  {"mac": "B4:79:C8:38:B1:C8", "nome": "WLL-Inatel", "x": "10", "y": "5"},
  {"mac": "B4:79:C8:38:C0:B8", "nome": "WLL-Inatel", "x": "0", "y": "1"},
  {"mac": "B4:79:C8:39:31:28", "nome": "WLL-Inatel", "x": "0", "y": "1"},
  {"mac": "30:87:D9:42:FA:C8", "nome": "WLL-CDGHub", "x": "5", "y": "2"},
  {"mac": "6C:14:6E:3E:DB:50", "nome": "wlanaccessv2.0", "x": "0", "y": "1"},
  {"mac": "6C:14:6E:3E:DF:10", "nome": "wlanaccessv2.0", "x": "0", "y": "1"},
  {"mac": "6C:14:6E:3E:DB:51", "nome": "Huawei-Employee", "x": "0", "y": "1"},
  {"mac": "6C:14:6E:3E:DB:52", "nome": "Huawei-Employee", "x": "0", "y": "1"},
  {"mac": "6C:14:6E:3E:DE:71", "nome": "Huawei-Employee", "x": "0", "y": "1"},
  {"mac": "6C:14:6E:3E:DE:72", "nome": "Huawei-Employee", "x": "0", "y": "1"},
  {"mac": "B4:79:C8:45:C2:38", "nome": "Inatel-BRDC-V", "x": "0", "y": "1"},
  {"mac": "B4:79:C8:45:C2:78", "nome": "Inatel-BRDC-V", "x": "0", "y": "1"},
  {"mac": "B4:79:C8:78:B1:C8", "nome": "Inatel-BRDC-V", "x": "8", "y": "3"},
  {"mac": "E8:1D:A8:30:F1:E8", "nome": "Inatel-BRDC-V", "x": "0", "y": "1"}
]

mac1 = db.reference('/networks/0')
mac2 = db.reference('/networks/1')
mac3 = db.reference('/networks/2')

data1 = mac1.get()
data2 = mac2.get()
data3 = mac3.get()

x1, y1 = compararMac(redes,data1["mac"])
x2, y2 = compararMac(redes,data2["mac"])
x3, y3 = compararMac(redes,data3["mac"])

if(data1 != None or data1 != None or data1 != None):
  x, y = triangulacao(int(x1),int(y1), data1["rssi"], int(x2),int(y2), data2["rssi"], int(x3),int(y3), data3["rssi"])
  print(f"X: {x}m")
  print(f"Y: {y}m")

