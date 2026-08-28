#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

// Networking
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* serverUrl = "http://YOUR_BACKEND_IP:8000/api/sensors";

// Device Info
const String deviceId = "esp32-node-001";

// Pins
#define DHTPIN 4
#define DHTTYPE DHT22
#define MQ135_PIN 34
#define MQ9_PIN 35
#define FLAME_PIN 32
#define TRIG_PIN 5
#define ECHO_PIN 18

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  
  pinMode(MQ135_PIN, INPUT);
  pinMode(MQ9_PIN, INPUT);
  pinMode(FLAME_PIN, INPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  dht.begin();
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected!");
}

float getWaterDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  // 30ms timeout (max ~5 meters) to prevent loop blocking if echo is lost
  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  if (duration == 0) return 200.0; // Default baseline on timeout
  float distance = duration * 0.034 / 2.0;
  return distance;
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    float temp = dht.readTemperature();
    float hum = dht.readHumidity();
    
    // Guard against DHT NaN read failures
    if (isnan(temp)) temp = 25.0;
    if (isnan(hum)) hum = 50.0;

    int mq135 = analogRead(MQ135_PIN);
    int mq9 = analogRead(MQ9_PIN);
    bool flame = digitalRead(FLAME_PIN) == LOW; // Active Low trigger
    float distance = getWaterDistance();

    String payload = "{";
    payload += "\"device_id\":\"" + deviceId + "\",";
    payload += "\"temperature\":" + String(temp) + ",";
    payload += "\"humidity\":" + String(hum) + ",";
    payload += "\"mq135_air_quality\":" + String(mq135) + ",";
    payload += "\"mq9_gas_level\":" + String(mq9) + ",";
    payload += "\"flame_detected\":" + String(flame ? "true" : "false") + ",";
    payload += "\"water_distance_cm\":" + String(distance);
    payload += "}";

    int httpResponseCode = http.POST(payload);
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    
    http.end();
  }
  
  delay(5000); // Send data every 5 seconds
}
