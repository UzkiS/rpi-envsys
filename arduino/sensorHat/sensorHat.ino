/*

*/

#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <Wire.h>
#include <Adafruit_SGP30.h>
#include <SoftwareSerial.h>
#include <math.h>
#define DHTPIN  4
#define DHTTYPE DHT11
#define RX  2
#define TX  3
SoftwareSerial Serial1(RX, TX); 
DHT_Unified dht(DHTPIN, DHTTYPE);
Adafruit_SGP30 sgp;
uint32_t delayMS;
byte serialIn[64];
uint32_t a;
uint32_t hchoHightNum, hchoLowNum;
uint32_t tvocHightNum, tvocLowNum;
uint32_t eco2HightNum, eco2LowNum;
uint32_t DHTStatus = 0;
uint32_t hchoStatus = 0;
float dhtTemperature, dhtHumidity;
uint32_t dhtTemp, dhtHumi;
uint32_t hchoSum = 0;
uint32_t checkSum = 0;


// unsigned char CheckSum(uchar *i,uncharln)

// the setup routine runs once when you press reset:
void setup() {
    Serial.begin(9600);
    Serial1.begin(9600);
    dht.begin();
}

// the loop routine runs over and over again forever:
void loop() {
    delay(2000);
    if(Serial1.available() > 0){
        Serial1.readBytes(serialIn,Serial1.available());	
        for (size_t i = 1; i <= 7; i++)
        {
            hchoSum += serialIn[i];
        }
        if (serialIn[0] == 0xFF && serialIn[8] == byte(~(hchoSum)+1))
        {
            //Serial.println("数据校验成功");
            hchoHightNum = serialIn[4];
            hchoLowNum = serialIn[5];
            //Serial.print(hchoC);
            //Serial.println("ppb ");
        }else
        {
            hchoHightNum = 0xEE;
            hchoLowNum = 0xEE;
            //Serial.println("数据校验失败");
        }

    }else
    {
        hchoHightNum = 0xEE;
        hchoLowNum = 0xEE;
    }
    
    hchoSum = 0;

    // Get temperature event and print its value.
    sensors_event_t dhtEvent;
    dht.temperature().getEvent(&dhtEvent);
    if (isnan(dhtEvent.temperature)) {
        //Serial.println(F("Error reading temperature!"));
        dhtTemp = 0xEE;
    }
    else {
        dhtTemperature = dhtEvent.temperature;
        dhtTemp = floor(dhtTemperature);
        //Serial.print(F("Temperature: "));
        //Serial.print(dhtEvent.temperature);
        //Serial.println(F("°C"));
    }
    // Get humidity event and print its value.
    dht.humidity().getEvent(&dhtEvent);
    if (isnan(dhtEvent.relative_humidity)) {
        //Serial.println(F("Error reading humidity!"));
        dhtHumi = 0xEE;
    }
    else {
        dhtHumidity = dhtEvent.relative_humidity;
        dhtHumi = floor(dhtHumidity);

        //Serial.print(F("Humidity: "));
        //Serial.print(dhtEvent.relative_humidity);
        //Serial.println(F("%"));
    }


    tvocHightNum = 0x01;
    tvocLowNum = 0x02;
    eco2HightNum = 0x01;
    eco2LowNum = 0x02;

    checkSum = ~(hchoHightNum + hchoLowNum + dhtTemp + dhtHumi + tvocHightNum + tvocLowNum +eco2HightNum +eco2LowNum) + 1;

    Serial.write(0xFF);
    Serial.write(hchoHightNum);
    Serial.write(hchoLowNum);
    Serial.write(dhtTemp);
    Serial.write(dhtHumi);
    Serial.write(tvocHightNum);
    Serial.write(tvocLowNum);
    Serial.write(eco2HightNum);
    Serial.write(eco2LowNum);
    Serial.write(0x00);
    Serial.write(0x00);
    Serial.write(checkSum);
    
    
}