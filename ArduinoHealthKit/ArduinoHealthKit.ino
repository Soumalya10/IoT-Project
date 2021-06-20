#include "config.h"
float temperature=0;
double ecg=0;
String serverName = "https://api.thingspeak.com/update?api_key=FL36D2MOEQ9HTM86";
MAX30105 ptox;
void setup() {
  //Board Setup
  pinMode(LED_W,OUTPUT);pinMode(LED_S,OUTPUT);pinMode(LED_K,OUTPUT);
  pinMode(15,INPUT);pinMode(32,INPUT);//EEG
  delay(100);
  // Network Setup
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
   delay(1000);
  }
  digitalWrite(LED_W,1);
  //MAX30105 Sensor Initilization
    if (!ptox.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    while (1);
  }
  byte ledBrightness = 60; //Options: 0=Off to 255=50mA
  byte sampleAverage = 4; //Options: 1, 2, 4, 8, 16, 32
  byte ledMode = 2; //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
  byte sampleRate = 100; //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
  int pulseWidth = 411; //Options: 69, 118, 215, 411
  int adcRange = 4096; //Options: 2048, 4096, 8192, 16384
  ptox.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange); 
  ptox.setPulseAmplitudeGreen(0); //Turn off Green LED
  ptox.enableDIETEMPRDY(); //Enable the temp ready interrupt
  //AD ECG Config
    while (digitalRead(17)==1 || digitalRead(32)==1)
    {
    continue;
    }
  digitalWrite(LED_S,HIGH);
  
  //Cloud Based Entry Config
  String serverName = "https://api.thingspeak.com/update?api_key=FL36D2MOEQ9HTM86";
  unsigned long lastTime = 0;
  unsigned long timerDelay = 1000;
  unsigned long timerEEG = 100;
  

}

void loop() {
  // put your main code here, to run repeatedly:
    temperature = ptox.readTemperature();
    bufferLength = 100; //buffer length of 100 stores 4 seconds of samples running at 25sps

  //read the first 100 samples, and determine the signal range
  for (byte i = 0 ; i < bufferLength ; i++)
  {
    while (ptox.available() == false) //do we have new data?
      ptox.check(); //Check the sensor for new data
      redBuffer[i] = ptox.getRed();
      irBuffer[i] = ptox.getIR();
      ptox.nextSample(); //We're finished with this sample so move to next sample
  }

  //calculate heart rate and SpO2 and temperature after first 100 samples (first 4 seconds of samples)
  maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
  
  if (validSPO2>0&&validHeartRate>0)
  {
    sendPTO(spo2,heartRate,temperature);
  }
    while (1)
  {
    //dumping the first 25 sets of samples in the memory and shift the last 75 sets of samples to the top
    for (byte i = 25; i < 100; i++)
    {
      redBuffer[i - 25] = redBuffer[i];
      irBuffer[i - 25] = irBuffer[i];
    }

    //take 25 sets of samples before calculating the heart rate.
    for (byte i = 75; i < 100; i++)
    {
      while (ptox.available() == false) //do we have new data?
        {
          ptox.check(); //Check the sensor for new data
          
        }
      ecg = analogRead(adpin);
      sendECG(ecg);//Schedule ECG Task Delay 1s implied
      redBuffer[i] = ptox.getRed();
      irBuffer[i] = ptox.getIR();
      ptox.nextSample(); //We're finished with this sample so move to next sample
    }
    temperature = ptox.readTemperature();
    //After gathering 25 new samples recalculate HR and SP02
    maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
      if (validSPO2>0&&validHeartRate>0)
        {
          sendPTO(spo2,heartRate,temperature);
        }
  }

}
void sendECG(double ecg)
{
  HTTPClient http;
  String url = serverName+"&field4=" +String(ecg);
  http.begin(url.c_str());
  int httpResponseCode = http.GET();
  if(httpResponseCode==0)
  digitalWrite(LED_K,HIGH);
  else
  digitalWrite(LED_K,LOW);
  http.end();
}
void sendPTO(int32_t O,float T,int32_t P)
{
  HTTPClient http;
  String url =serverName + "&field1=" + String(P) + "&field2=" + String(T) + "&field3=" + String(O);
  http.begin(url.c_str());
  int httpResponseCode = http.GET();
  if(httpResponseCode==0)
  digitalWrite(LED_K,HIGH);
  else
  digitalWrite(LED_K,LOW);
  http.end();
}
