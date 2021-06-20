#ifndef CONFIG_H
#include <heartRate.h>
#include <MAX30105.h>
#include <spo2_algorithm.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
//Board Configartion
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
const int LED_W = 25;
const int LED_S = 26;
const int LED_K = 27;
const int adpin = 36;
#define MAX_BRIGHTNESS 255
//Config for HeartRate
//SPo2
uint32_t irBuffer[100]; //infrared LED sensor data
uint32_t redBuffer[100];  //red LED sensor data
int32_t bufferLength; //data length
int32_t spo2; //SPO2 value
int8_t validSPO2; //indicator to show if the SPO2 calculation is valid
int32_t heartRate; //heart rate value
int8_t validHeartRate; //indicator to show if the heart rate calculation is valid
#endif
