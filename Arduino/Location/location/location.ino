
#include <Arduino.h>

// Inclusões de bibliotecas dependendo do dispositivo
#if defined(ESP32) || defined(ARDUINO_RASPBERRY_PI_PICO_W)
#include <WiFi.h>
#elif defined(ESP8266)
#include <ESP8266WiFi.h>
#endif

#include <Firebase_ESP_Client.h>
#include <addons/TokenHelper.h>
#include <addons/RTDBHelper.h>

// Informações da rede Wi-Fi e configurações do Firebase
#define WIFI_SSID "Pedro"
#define WIFI_PASSWORD "ronk1234"
#define API_KEY "AIzaSyBQJUY7-kt1dBgn5FjeES1o_Bc_G-8AU6o"
#define DATABASE_URL "https://esp8266-2dca6-default-rtdb.firebaseio.com/"
#define USER_EMAIL "ppg108@hotmail.com"
#define USER_PASSWORD "1594875pedro"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

// Número máximo de redes e valores RSSI
const int MAX_NETWORKS = 50;
const int MAX_RSSI_VALUES = 50;

// Intervalo de medição
const int MEASURE_INTERVAL = 100;

// Estrutura para armazenar informações da rede
struct Network {
  String macAddress;
  String bssid;
  int rssiValues[MAX_RSSI_VALUES];
  int numValues;
  float avgRssi;
};

Network networks[MAX_NETWORKS];
int numNetworks = 0;

// Variáveis para controle de envio e contagem
unsigned long sendDataPrevMillis = 0;
unsigned long count = 0;

// Função para inserir informações de uma nova rede
void insertNetworkInfo(const String &mac, const String &bssid) {
  Network newNetwork;
  newNetwork.macAddress = mac;
  newNetwork.bssid = bssid;
  numNetworks++;
}

// Wi-Fi Multi para o Raspberry Pi Pico
#if defined(ARDUINO_RASPBERRY_PI_PICO_W)
WiFiMulti multi;
#endif

void setup() {

  Serial.begin(115200);

  // Inserção das redes do Inatel
  insertNetworkInfo("20:58:69:0E:AA:38", "WLL-Inatel");

  // Iniciar conexão Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("Connecting to Wi-Fi");
  unsigned long ms = millis();
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
    // Adicionar condição de timeout, se necessário
    if (millis() - ms > 10000) {
      break;
    }
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);

  // Configurar Firebase
  config.api_key = API_KEY;
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;
  config.database_url = DATABASE_URL;
  config.token_status_callback = tokenStatusCallback;

  // Ajustar configurações Firebase
  fbdo.setResponseSize(2048);
  Firebase.begin(&config, &auth);

  // Reconectar Wi-Fi (caso necessário)
  Firebase.reconnectWiFi(true);
  Firebase.setDoubleDigits(5);
  config.timeout.serverResponse = 10 * 1000;
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

      Serial.println(mac);
      Serial.println(bssid);
      Serial.println(rssi);
      Serial.println(networks[i].macAddress);

      if (networks[i].macAddress == mac) {
        networks[i].rssiValues[networks[i].numValues] = rssi;
        networks[i].numValues++;
      }
    }
  }

  for (int i = 0; i < numNetworks; i++) {
    FirebaseJson json;
    float sumRssi = 0;
    int numValues = networks[i].numValues;
    int startIndex = numValues > MAX_RSSI_VALUES ? numValues - MAX_RSSI_VALUES : 0;
    for (int j = startIndex; j < numValues; j++) {
      sumRssi += networks[i].rssiValues[j];
    }
    if ((numValues - startIndex) > 0) {
      networks[i].avgRssi = sumRssi / (numValues - startIndex);
    }
    if (Firebase.ready() || sendDataPrevMillis == 0) {
      sendDataPrevMillis = millis();

      String mackey_add = "networks/" + networks[i].macAddress + "/mac";
      String mackey_bssid = "networks/" + networks[i].macAddress + "/bssid";
      String mackey_rssi = "networks/" + networks[i].macAddress + "/rssi";

      Serial.printf("SET MAC. %s\n", Firebase.RTDB.setString(&fbdo, mackey_add.c_str(), networks[i].macAddress) ? "oK" : fbdo.errorReason().c_str());
      Serial.printf("SET BSSID. %s\n", Firebase.RTDB.setString(&fbdo, mackey_bssid.c_str(), networks[i].bssid) ? "oK" : fbdo.errorReason().c_str());
      Serial.printf("SET AVG RSSI. %s\n", Firebase.RTDB.setFloat(&fbdo, mackey_rssi.c_str(), networks[i].avgRssi) ? "oK" : fbdo.errorReason().c_str());
    }
  }
}
