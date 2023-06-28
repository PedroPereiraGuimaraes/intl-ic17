
#include <Arduino.h>

#if defined(ESP32) || defined(ARDUINO_RASPBERRY_PI_PICO_W)
#include <WiFi.h>
#elif defined(ESP8266)
#include <ESP8266WiFi.h>
#endif

#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>
#include <Firebase_ESP_Client.h>
#include <addons/TokenHelper.h>
#include <addons/RTDBHelper.h>


#define WIFI_SSID "WLL-Inatel"
#define WIFI_PASSWORD "inatelsemfio"

#define API_KEY "AIzaSyBQJUY7-kt1dBgn5FjeES1o_Bc_G-8AU6o"

#define DATABASE_URL "https://esp8266-2dca6-default-rtdb.firebaseio.com/"

#define USER_EMAIL "ppg108@hotmail.com"
#define USER_PASSWORD "1594875pedro"

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

const int MAX_NETWORKS = 50;
const int MAX_RSSI_VALUES = 50;
const int MEASURE_INTERVAL = 100;  // 10 segundos

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

#if defined(ARDUINO_RASPBERRY_PI_PICO_W)
WiFiMulti multi;
#endif

void setup() {

  Serial.begin(115200);

  ntpUDP.begin(2390);
  timeClient.begin();
  timeClient.setTimeOffset(-3 * 3600);


#if defined(ARDUINO_RASPBERRY_PI_PICO_W)
  multi.addAP(WIFI_SSID, WIFI_PASSWORD);
  multi.run();
#else
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
#endif

  Serial.print("Connecting to Wi-Fi");
  unsigned long ms = millis();
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
#if defined(ARDUINO_RASPBERRY_PI_PICO_W)
    if (millis() - ms > 10000)
      break;
#endif
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the user sign in credentials */
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback;  // see addons/TokenHelper.h


#if defined(ESP8266)
  // In ESP8266 required for BearSSL rx/tx buffer for large data handle, increase Rx size as needed.
  fbdo.setBSSLBufferSize(2048 /* Rx buffer size in bytes from 512 - 16384 */, 2048 /* Tx buffer size in bytes from 512 - 16384 */);
#endif

  // Limit the size of response payload to be collected in FirebaseData
  fbdo.setResponseSize(2048);

  Firebase.begin(&config, &auth);

  // The WiFi credentials are required for Pico W
  // due to it does not have reconnect feature.
#if defined(ARDUINO_RASPBERRY_PI_PICO_W)
  config.wifi.clearAP();
  config.wifi.addAP(WIFI_SSID, WIFI_PASSWORD);
#endif

  // Comment or pass false value when WiFi reconnection will control by your code or third party library
  Firebase.reconnectWiFi(true);
  Firebase.setDoubleDigits(5);
  config.timeout.serverResponse = 10 * 1000;
}

void loop() {

  timeClient.update();

  time_t currentTime = timeClient.getEpochTime();

  tm* timeinfo = localtime(&currentTime);

  int day = timeinfo->tm_mday;

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
        if (numNetworks < MAX_NETWORKS) {
          Network newNetwork;
          newNetwork.macAddress = mac;
          newNetwork.bssid = bssid;
          newNetwork.rssiValues[0] = rssi;
          newNetwork.numValues = 1;
          networks[numNetworks] = newNetwork;
          numNetworks++;
        } else {
          Serial.println("Limite máximo de redes atingido.");
        }
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
      Serial.print("MAC: " + networks[i].macAddress);
      Serial.print("\nNome da Rede: " + networks[i].bssid + "\nRssi: ");
      Serial.println(networks[i].avgRssi);
    }
    if (Firebase.ready() || sendDataPrevMillis == 0) {
      sendDataPrevMillis = millis();
      String time = timeClient.getFormattedTime();
      String local = "biblioteca";

      String mackey_add = "training/" + String(local) + "/" +  networks[i].macAddress + "/mac";
      String mackey_bssid = "training/" + String(local) + "/" +  networks[i].macAddress + "/bssid";
      String mackey_rssi = "training/" + String(local) + "/" +  networks[i].macAddress + "/rssi";

      Serial.printf("SET MAC. %s\n", Firebase.RTDB.setString(&fbdo, mackey_add.c_str(), networks[i].macAddress) ? "oK" : fbdo.errorReason().c_str());
      Serial.printf("SET BSSID. %s\n", Firebase.RTDB.setString(&fbdo, mackey_bssid.c_str(), networks[i].bssid) ? "oK" : fbdo.errorReason().c_str());
      Serial.printf("SET AVG RSSI. %s\n", Firebase.RTDB.setFloat(&fbdo, mackey_rssi.c_str(), networks[i].avgRssi) ? "oK" : fbdo.errorReason().c_str());
    }
  }
}
