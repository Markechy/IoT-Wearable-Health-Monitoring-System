#include <ESP8266WiFi.h>
#include <Wire.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

WiFiClient espClient;
PubSubClient client(espClient);

#define NEO 14
#define SEL 12
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define TIME_POSITION_X 10
#define TIME_POSITION_Y 20
#define TEXT_SIZE 4

Adafruit_NeoPixel strip = Adafruit_NeoPixel(16, NEO, NEO_GRB + NEO_KHZ800);

const char* SSID = "realme GT 2 Pro";
const char* PASSWORD = "gejejhejeh3gh";
const char* MQTT_SERVER = "192.168.95.172";
const char* CLIENT_ID = "ESP8266-EQUIPO-99";
const int MQTT_BROKER_PORT = 1883;

const char* topic1 = "heartrate";
const char* topic2 = "spo2";
const char* topic3 = "temp";
const char* topic4 = "hum";
const char* topic5 = "esps";

char x = '0';
int mode = 0;
int y = 0;
int one = 0;

char heart[4];
char pulse[4];
char temp[4];
char hum[4];

void setup() {
  Serial.begin(9600);
  strip.begin();
  strip.setBrightness(255);
  NeoSet(0, 0, 0);
  strip.show();
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    while (1);
  }
  pinMode(SEL, INPUT);
  setup_wifi();
  client.setServer(MQTT_SERVER, MQTT_BROKER_PORT);
  client.setCallback(callback);
  display.clearDisplay();
  display.setTextSize(TEXT_SIZE);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(TIME_POSITION_X, TIME_POSITION_Y);
  display.display();
}

void loop() {
  display.clearDisplay();
  if (!client.connected()) {
    reconnect();
  }
  if (!client.loop()) {
    client.connect(CLIENT_ID);
  }

  if (x == '6' and mode == 0) {
    NeoSet(0, 0, 0);
    strip.setPixelColor(y, 54, 255, 32);
    strip.show();
    if (y <= 16) {
      y++;
    } else {
      y = 0;
    }
    delay(50);
  }

  if (x == '1') {
    Serial.write(0x01);
    for (int i = 0; i <= 255; i++) {
      NeoSet(i, i, i);
      strip.show();
      delay(50);
    }
    x = '6';
    mode = 1;
  }

  if (mode == 1) {
    NeoSet(0, 155, 205);
    strip.show();
    display.clearDisplay();
    display.setTextSize(TEXT_SIZE);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(TIME_POSITION_X, TIME_POSITION_Y);
    display.print(1);
    display.print(":");
    display.print(32);
    display.display();
  } else if (mode == 2) {
    NeoSet(255, 0, 0);
    strip.show();
    display.clearDisplay();
    display.setTextSize(TEXT_SIZE);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(TIME_POSITION_X, TIME_POSITION_Y);
    display.print(heart[0]);
    display.print(heart[1]);
    display.print(heart[2]);
    display.print(heart[3]);
    display.display();
  } else if (mode == 3) {
    NeoSet(0, 0, 255);
    strip.show();
    display.clearDisplay();
    display.setTextSize(TEXT_SIZE);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(TIME_POSITION_X, TIME_POSITION_Y);
    display.print(pulse[0]);
    display.print(pulse[1]);
    display.print(pulse[2]);
    display.print(pulse[3]);
    display.display();
  } else if (mode == 4) {
    NeoSet(204, 255, 0);
    display.clearDisplay();
    display.setTextSize(TEXT_SIZE);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(TIME_POSITION_X, TIME_POSITION_Y);
    display.print(temp[0]);
    display.print(temp[1]);
    display.print(temp[2]);
    display.print(temp[3]);
    display.display();
    strip.show();
  } else if (mode == 5) {
    NeoSet(0, 255, 0);
    strip.show();
    display.clearDisplay();
    display.setTextSize(TEXT_SIZE);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(TIME_POSITION_X, TIME_POSITION_Y);
    display.print(hum[0]);
    display.print(hum[1]);
    display.print(hum[2]);
    display.print(hum[3]);
    display.display();
  } else if (mode == 6) {
    mode = 1;
  }

  if (digitalRead(SEL) == 1) {
    delay(200);
    mode++;
  }
}

void setup_wifi() {
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    NeoSet(0, 0, 0);
    strip.setPixelColor(y, 54, 255, 32);
    strip.show();
    if (y <= 16) {
      y++;
    } else {
      y = 0;
    }
    delay(50);
  }
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect(CLIENT_ID)) {
      client.subscribe(topic5);
      client.subscribe(topic1);
      client.subscribe(topic2);
      client.subscribe(topic3);
      client.subscribe(topic4);
      if(one == 0){
        char t[10];
        sprintf(t, "%d", 'A');
        client.publish(topic5, t);
        one++;
      }
    } else {
      delay(50);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  if (String(topic) == "esps") {
    x = (char)payload[0];
  } else if (String(topic) == "heartrate") {
    heart[0] = 0;
    heart[1] = 0;
    heart[2] = 0;
    heart[3] = 0;
    heart[0] = (char)payload[0];
    heart[1] = (char)payload[1];
    heart[2] = (char)payload[2];
    heart[3] = (char)payload[3];
  } else if (String(topic) == "spo2") {
    pulse[0] = 0;
    pulse[1] = 0;
    pulse[2] = 0;
    pulse[3] = 0;
    pulse[0] = (char)payload[0];
    pulse[1] = (char)payload[1];
    //pulse[2] = (char)payload[2];
    //pulse[3] = (char)payload[3];
  } else if (String(topic) == "temp") {
    temp[0] = 0;
    temp[1] = 0;
    temp[2] = 0;
    temp[3] = 0;
    temp[0] = (char)payload[0];
    temp[1] = (char)payload[1];
    //temp[2] = (char)payload[2];
    //temp[3] = (char)payload[3];
  } else if (String(topic) == "hum") {
    hum[0] = 0;
    hum[1] = 0;
    hum[2] = 0;
    hum[3] = 0;
    hum[0] = (char)payload[0];
    hum[1] = (char)payload[1];
    hum[2] = (char)payload[2];
    hum[3] = (char)payload[3];
  }
}

void NeoSet(int r, int g, int b) {
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, r, g, b);
  }
}
