#include <ESP8266WiFi.h>

const int MAX_NETWORKS = 20;
const int MAX_RSSI_VALUES = 30;
const int MEASURE_INTERVAL = 3000; // 10 segundos

struct Network {
  String macAddress;
  String bssid;
  int rssiValues[MAX_RSSI_VALUES];
  int numValues;
  float avgRssi;
};

float rssiParaDistancia(int rssi) {

  float a = -50;
  float w = (rssi - a) / -40.0;
  float distancia = pow(10, w);
  
  return distancia;
}

Network networks[MAX_NETWORKS];
int numNetworks = 0;

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  delay(10);
}

void loop() {
  int n = WiFi.scanNetworks();
  if (n == 0) {
    Serial.println("No networks found");
  } else {
    for (int i = 0; i < n; i++) {
      String mac = WiFi.BSSIDstr(i);
      String bssid = WiFi.SSID(i);
      int rssi = WiFi.RSSI(i);
      // check if network already exists
      bool found = false;
      for (int j = 0; j < numNetworks; j++) {
        if (networks[j].macAddress == mac) {
          // add RSSI value to existing network
          networks[j].rssiValues[networks[j].numValues] = rssi;
          networks[j].numValues++;
          found = true;
          break;
        }
      }
      if (!found) {
        // create new network and add RSSI value
        Network newNetwork;
        newNetwork.macAddress = mac;
        newNetwork.bssid = bssid;
        newNetwork.rssiValues[0] = rssi;
        newNetwork.numValues = 1;
        networks[numNetworks] = newNetwork;
        numNetworks++;
      }
    }
  }

  // calculate average RSSI for each network every MEASURE_INTERVAL
  static unsigned long lastMeasureTime = 0;
  static unsigned long lastResetTime = 0;
  unsigned long now = millis();
  if (now - lastResetTime >= MEASURE_INTERVAL) {
    // reset averages
    for (int i = 0; i < numNetworks; i++) {
      networks[i].avgRssi = 0;
      networks[i].numValues = 0;
    }
    lastResetTime = now;
  }
  if (now - lastMeasureTime >= 1000) { // calculate average every second
    Serial.println("Calculating average RSSI");
    Serial.println("-----------------------\n\n");
    for (int i = 0; i < numNetworks; i++) {
      float sumRssi = 0;
      int numValues = networks[i].numValues;
      int startIndex = numValues > MAX_RSSI_VALUES ? numValues - MAX_RSSI_VALUES : 0;
      for (int j = startIndex; j < numValues; j++) {
        sumRssi += networks[i].rssiValues[j];
      }
      if ((numValues - startIndex) > 0) {
        networks[i].avgRssi = sumRssi / (numValues - startIndex);
        Serial.print("MAC:" + networks[i].macAddress);
        Serial.print("\nNome da Rede: " + networks[i].bssid + "\nRssi:");
        Serial.println(networks[i].avgRssi);
        Serial.println("Distância do Modem é de " + String(rssiParaDistancia(networks[i].avgRssi)) + " metros.");
        Serial.println("-----------------------\n");
      }
    }
    lastMeasureTime = now;
  }
  delay(10);
}
