#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

// Reemplaza con los datos de tu red
 const char* ssid = "TIGO-43C0";
 const char* password = "4NJ667302283";
//const char* ssid = "Josh10";
//const char* password = "Guate2025!";

// Pines para el sensor DHT11
#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// Dirección IPv6 del servidor virtual (esta es una dirección de ejemplo)
// Reemplaza con la dirección IPv6 real de tu máquina virtual una vez configurada
// const char* serverAddress = "http://[fd00:db8:1::1]/api/datos"; // IPv6
// const char* serverAddress = "http://[fd00:db8:1::1]:5000/api/datos"; // IPv6
 const char* serverAddress = "http://httpbin.org/post"; // IPv4

void setup() {
  
  Serial.begin(115200);

  // Iniciar la conexión WiFi
  Serial.println("Conectando a la red WiFi...");
  WiFi.begin(ssid, password);

  // Esperar la conexión
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando...");
  }
  
  Serial.println("¡Conectado a la red!");
  //Serial.print("Dirección IPv6: ");
  Serial.println(WiFi.localIP()); // IPv4
  //Serial.println(WiFi.localIPv6()); // IPv6

  dht.begin();
}

void loop() {
  // Espera 5 segundos entre lecturas
  delay(5000);

  // Lectura de los valores del sensor
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // Verifica si la lectura fue exitosa
  if (isnan(h) || isnan(t)) {
    Serial.println("Error al leer el sensor DHT11.");
    return;
  }

  // Creación del objeto JSON para enviar los datos
  String jsonPayload = "{\"temperatura\":";
  jsonPayload += t;
  jsonPayload += ",\"humedad\":";
  jsonPayload += h;
  jsonPayload += "}";

  // Envío de la petición HTTP POST
  HTTPClient http;
  http.begin(serverAddress);
  http.addHeader("Content-Type", "application/json");

  Serial.println("Enviando datos al servidor...");
  int httpResponseCode = http.POST(jsonPayload);

  // Comprueba el resultado de la petición
  if (httpResponseCode > 0) {
    Serial.printf("Respuesta del servidor: %d\n", httpResponseCode);
    String response = http.getString();
    Serial.println(response);
  } else {
    Serial.printf("Error al enviar la petición: %d\n", httpResponseCode);
  }

  http.end();
}