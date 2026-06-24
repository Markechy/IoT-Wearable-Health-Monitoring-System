#include <ESP8266WiFi.h>
#include <Wire.h>
#include <DFRobot_MAX30102.h>
#include <PubSubClient.h>
#include <Adafruit_AHT10.h>

DFRobot_MAX30102 particleSensor;

WiFiClient espClient;
PubSubClient client(espClient);
Adafruit_AHT10 aht;

const char* SSID = "realme GT 2 Pro";
const char* PASSWORD = "gejejhejeh3gh";
const char* MQTT_SERVER = "192.168.95.172";
const char* CLIENT_ID = "ESP8266-EQUIPO-9";
const int MQTT_BROKER_PORT = 1883;

const char* topic1 = "heartrate";
const char* topic2 = "spo2";
const char* topic3 = "temp";
const char* topic4 = "hum";
const char* topic5 = "esps";

int one = 0;

int32_t SPO2;
int8_t SPO2Valid;
int32_t heartRate;
int8_t heartRateValid;

void setup()
{
  //Serial.begin(115200);
  while (!particleSensor.begin(&Wire, 0x57))
  {
    //Serial.println("MAX30102 was not found");
    delay(1000);
  }
  while (!aht.begin(&Wire, 0x38))
  {
    //Serial.println("AHT10 was not found");
    delay(1000);
  }
  particleSensor.sensorConfiguration(96, SAMPLEAVG_4, MODE_MULTILED, SAMPLERATE_100, PULSEWIDTH_411, ADCRANGE_16384);
  setup_wifi();
  client.setServer(MQTT_SERVER, MQTT_BROKER_PORT);
  //Serial.write(1);
  //Serial.println("Ya");
}

void loop()
{
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);
  //Serial.print("Temperature: "); Serial.print(temp.temperature); Serial.println(" degrees C");
  //Serial.print("Humidity: "); Serial.print(humidity.relative_humidity); Serial.println("% rH");

  particleSensor.heartrateAndOxygenSaturation(&SPO2, &SPO2Valid, &heartRate, &heartRateValid);
  //Serial.print(F("heartRate="));
  //Serial.print(heartRate, DEC);
  //Serial.print(F(", heartRateValid="));
  //Serial.print(heartRateValid, DEC);
  //Serial.print(F("\tspo2="));
  //Serial.print(SPO2, DEC);
  //Serial.print(F(", spo2Valid="));
  //Serial.print(SPO2Valid, DEC);
  //Serial.print(F("\n"));

  if (!client.connected())
  {
    reconnect();
  }
  if(!client.loop())
  {
    client.connect(CLIENT_ID);
  }

  if (one == 0) {
    char x[10];
    sprintf(x, "%d", 'd');
    client.publish(topic5, x);
    one++;
  }

  char payload[10];
  if(heartRate >= 60 and heartRate < 100) {
    sprintf(payload, "%d", heartRate);
    client.publish(topic1, payload);
    delay(100);
  }
  if(SPO2 >= 20 and SPO2 <= 100) {
    sprintf(payload, "%d", SPO2);
    client.publish(topic2, payload);
    delay(100);
  }
  sprintf(payload, "%.2f", temp.temperature);
  client.publish(topic3, payload);
  delay(50);
  sprintf(payload, "%.2f", humidity.relative_humidity);
  client.publish(topic4, payload);
}

void setup_wifi() {
  //Serial.println();
  //Serial.print("Connecting to ");
  //Serial.println(SSID);
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    //Serial.print(".");
  }
  //Serial.println("");
  //Serial.print("WiFi connected - ESP IP address: ");
  //Serial.println(WiFi.localIP());
}

void reconnect()
{
  while (!client.connected())
  {
    //Serial.print("Attempting MQTT connection...");
    if (client.connect(CLIENT_ID))
    {
      //Serial.println("connected");
    }
    else
    {
      //Serial.print("MQTT connection failed, rc=");
      //Serial.print(client.state());
      //Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}
