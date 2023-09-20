#include <Arduino.h>

// Inclusões de bibliotecas dependendo do dispositivo
#if defined(ESP32) || defined(ARDUINO_RASPBERRY_PI_PICO_W)
#include <WiFi.h>  // Inclui a biblioteca WiFi para ESP32 e Raspberry Pi Pico
#elif defined(ESP8266)
#include <ESP8266WiFi.h>  // Inclui a biblioteca WiFi para ESP8266
#endif

#include <Firebase_ESP_Client.h>
#include <addons/TokenHelper.h>
#include <addons/RTDBHelper.h>

// Informações da rede Wi-Fi e configurações do Firebase
#define WIFI_SSID "WLL-Inatel"
#define WIFI_PASSWORD "inatelsemfio"
#define API_KEY "AIzaSyBQJUY7-kt1dBgn5FjeES1o_Bc_G-8AU6o"
#define DATABASE_URL "https://esp8266-2dca6-default-rtdb.firebaseio.com/"
#define USER_EMAIL "ppg108@hotmail.com"
#define USER_PASSWORD "1594875pedro"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

const int MAX_NETWORKS = 50;
const int MAX_RSSI_VALUES = 50;
const int MEASURE_INTERVAL = 50;

struct Network {
  String macAddress;
  String bssid;
  int rssiValues[MAX_RSSI_VALUES];
  int numValues;
  float avgRssi;
};

Network networks[MAX_NETWORKS];
int numNetworks = 0;
unsigned long sendDataPrevMillis = 0;
unsigned long count = 0;

void addNetwork(String mac, String bssid) {
  // Função para inserir informações de uma nova rede na estrutura de dados
  if (numNetworks < MAX_NETWORKS) {
    networks[numNetworks].macAddress = mac;
    networks[numNetworks].bssid = bssid;
    networks[numNetworks].numValues = 0;
    numNetworks++;
  }
}

void setup() {
  Serial.begin(115200);

  // Inserção das redes do Inatel
  addNetwork("20:58:69:0E:AA:38", "WLL-Inatel");
  addNetwork("30:87:D9:02:FA:C8", "WLL-Inatel");
  addNetwork("30:87:D9:02:FE:08", "WLL-Inatel");
  addNetwork("B4:79:C8:05:B9:38", "WLL-Inatel");
  addNetwork("B4:79:C8:05:B9:A8", "WLL-Inatel");
  addNetwork("B4:79:C8:05:C2:38", "WLL-Inatel");
  addNetwork("B4:79:C8:05:C2:78", "WLL-Inatel");
  addNetwork("B4:79:C8:38:B1:C8", "WLL-Inatel");
  addNetwork("B4:79:C8:38:C0:B8", "WLL-Inatel");
  addNetwork("B4:79:C8:39:31:28", "WLL-Inatel");
  addNetwork("30:87:D9:42:FA:C8", "WLL-CDGHub");
  addNetwork("6C:14:6E:3E:DB:50", "wlanaccessv2.0");
  addNetwork("6C:14:6E:3E:DF:10", "wlanaccessv2.0");
  addNetwork("6C:14:6E:3E:DB:51", "Huawei-Employee");
  addNetwork("6C:14:6E:3E:DB:52", "Huawei-Employee");
  addNetwork("6C:14:6E:3E:DE:71", "Huawei-Employee");
  addNetwork("6C:14:6E:3E:DE:72", "Huawei-Employee");
  addNetwork("B4:79:C8:45:C2:38", "Inatel-BRDC-V");
  addNetwork("B4:79:C8:45:C2:78", "Inatel-BRDC-V");
  addNetwork("B4:79:C8:78:B1:C8", "Inatel-BRDC-V");
  addNetwork("E8:1D:A8:30:F1:E8", "Inatel-BRDC-V");
  // Redes da minha casa
  //addNetwork("10:27:F5:20:86:C4", "Pedro");
  //addNetwork("B0:A7:B9:F1:91:0F", "Cassio");
  //addNetwork("C0:06:C3:21:97:C8", "Lidiane Moreira");
  //addNetwork("28:EE:52:38:0D:20", "TP-Link_Yoda");

  Serial.print("Connecting to Wi-Fi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  unsigned long ms = millis();
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
    if (millis() - ms > 10000) {
      break;
    }
  }

  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();
  Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);

  config.api_key = API_KEY;
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;
  config.database_url = DATABASE_URL;
  config.token_status_callback = tokenStatusCallback;
  fbdo.setResponseSize(2048);
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
  Firebase.setDoubleDigits(5);
  config.timeout.serverResponse = 10 * 1000;
}

void sendDataToFirebase(String mac[], float rssi[]) {

  // Função para enviar dados para o Firebase
  sendDataPrevMillis = millis();

  for (int i = 0; i < 3; i++) {
    String macKey = "networks/" + String(i) + "/mac";
    String rssiKey = "networks/" + String(i) + "/rssi";

    Serial.printf("SET MAC. %s\n", Firebase.RTDB.setString(&fbdo, macKey.c_str(), mac[i]) ? "OK" : fbdo.errorReason().c_str());
    Serial.printf("SET AVG RSSI. %s\n", Firebase.RTDB.setFloat(&fbdo, rssiKey.c_str(), rssi[i]) ? "OK" : fbdo.errorReason().c_str());
    Serial.println("");
  }
}

void updateNetworkData(String mac, String bssid, int rssi, String macMax[], float rssiMax[]) {

  // Função para atualizar os dados da rede na estrutura de dados
  for (int j = 0; j < numNetworks; j++) {
    if (networks[j].macAddress == mac) {
      int numValues = networks[j].numValues;
      networks[j].rssiValues[numValues] = rssi;
      networks[j].numValues++;

      int startIndex = numValues > MAX_RSSI_VALUES ? numValues - MAX_RSSI_VALUES : 0;
      float sumRssi = 0;

      for (int n = startIndex; n < numValues; n++) {
        sumRssi += networks[j].rssiValues[n];
      }

      if ((numValues - startIndex) > 0) {
        networks[j].avgRssi = sumRssi / (numValues - startIndex);


        if (sumRssi / (numValues - startIndex) > rssiMax[0]) {
          // Modificando os TOP RSSI
          rssiMax[2] = rssiMax[1];
          rssiMax[1] = rssiMax[0];
          rssiMax[0] = sumRssi / (numValues - startIndex);
          // Modificando os TOP MAC
          macMax[2] = macMax[1];
          macMax[1] = macMax[0];
          macMax[0] = mac;
        } else if (sumRssi / (numValues - startIndex) > rssiMax[1]) {
          // Modificando os TOP RSSI
          rssiMax[2] = rssiMax[1];
          rssiMax[1] = sumRssi / (numValues - startIndex);
          // Modificando os TOP MAC
          macMax[2] = macMax[1];
          macMax[1] = mac;
        } else if (sumRssi / (numValues - startIndex) > rssiMax[2]) {
          rssiMax[2] = sumRssi / (numValues - startIndex);
          macMax[2] = mac;
        }
      }
      if (Firebase.ready() || sendDataPrevMillis == 0) {
        sendDataToFirebase(macMax, rssiMax);
      }
    }
  }
}

void processNetworks(int numNetworks) {

  float rssiMax[3] = { -300, -300, -300 };
  String macMax[3] = { "None", "None", "None" };

  // Função para processar as redes WiFi escaneadas
  for (int i = 0; i < numNetworks; i++) {
    String mac = WiFi.BSSIDstr(i);
    String bssid = WiFi.SSID(i);
    int rssi = WiFi.RSSI(i);

    updateNetworkData(mac, bssid, rssi, macMax, rssiMax);
  }
}

void loop() {
  int numNetworks = WiFi.scanNetworks();
  if (numNetworks == 0) {
    Serial.println("No networks found");
  } else {
    processNetworks(numNetworks);
  }
}
