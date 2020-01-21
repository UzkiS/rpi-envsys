#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <Wire.h>
#include <Adafruit_SGP30.h>
#include <SoftwareSerial.h>
#include <math.h>
#include <ArduinoJson.h>
#define DHTPIN  4
#define DHTTYPE DHT11
#define RX  2
#define TX  3
SoftwareSerial serialSensor(RX, TX); 
DHT_Unified dht(DHTPIN, DHTTYPE);
Adafruit_SGP30 sgp;
uint32_t delayMS;
byte serialIn[64];
uint32_t a;
uint32_t hchoHightNum, hchoLowNum;
float dhtTemperature, dhtHumidity;
uint32_t hchoSum = 0;
uint32_t checkSum = 0;
int32_t formaldehydeData, temperatureData, humidityData, lightData;
String resultJson;
uint32_t getAbsoluteHumidity(float temperature, float humidity) {
    // approximation formula from Sensirion SGP30 Driver Integration chapter 3.15
    const float absoluteHumidity = 216.7f * ((humidity / 100.0f) * 6.112f * exp((17.62f * temperature) / (243.12f + temperature)) / (273.15f + temperature)); // [g/m^3]
    const uint32_t absoluteHumidityScaled = static_cast<uint32_t>(1000.0f * absoluteHumidity); // [mg/m^3]
    return absoluteHumidityScaled;
}


// the setup routine runs once when you press reset:
void setup() {
    Serial.begin(9600);
    serialSensor.begin(9600);
    dht.begin();
    //sgp.begin();
    //StaticJsonDocument<200> doc;
    // if (! sgp.begin()){
    //     Serial.println("SGP sensor not found :(");
    // }
    // Serial.print(sgp.serialnumber[0], HEX);
    // Serial.print(sgp.serialnumber[1], HEX);
    // Serial.println(sgp.serialnumber[2], HEX);
}

int counter = 0;
// the loop routine runs over and over again forever:
void loop() {
    delay(2000);
    //DART Start
    if(serialSensor.available() > 0){
        serialSensor.readBytes(serialIn,serialSensor.available());	
        for (size_t i = 1; i <= 7; i++)
        {
            hchoSum += serialIn[i];
        }
        if (serialIn[0] == 0xFF && serialIn[8] == byte(~(hchoSum)+1))
        {
            hchoHightNum = serialIn[4];
            hchoLowNum = serialIn[5];

            formaldehydeData = hchoHightNum * 256 + hchoLowNum;
        }else
        {
            formaldehydeData = -1;
        }

    }else
    {
        formaldehydeData = -1;
    }
    
    hchoSum = 0;

    // Get temperature event and print its value.
    sensors_event_t dhtEvent;
    dht.temperature().getEvent(&dhtEvent);
    if (isnan(dhtEvent.temperature)) {
        temperatureData = -1;
    }
    else {
        dhtTemperature = dhtEvent.temperature;
        temperatureData = floor(dhtTemperature);
        //Serial.print(F("Temperature: "));
        //Serial.print(dhtEvent.temperature);
        //Serial.println(F("°C"));
    }
    // Get humidity event and print its value.
    dht.humidity().getEvent(&dhtEvent);
    if (isnan(dhtEvent.relative_humidity)) {
        //Serial.println(F("Error reading humidity!"));
        humidityData = -1;
    }
    else {
        dhtHumidity = dhtEvent.relative_humidity;
        humidityData = floor(dhtHumidity);

        //Serial.print(F("Humidity: "));
        //Serial.print(dhtEvent.relative_humidity);
        //Serial.println(F("%"));
    }


    //SGP Start
    // If you have a temperature / humidity sensor, you can set the absolute humidity to enable the humditiy compensation for the air quality signals
    // float temperature = dhtTemperature; // [°C]
    // float humidity = dhtHumidity; // [%RH]
    // sgp.setHumidity(getAbsoluteHumidity(dhtTemperature, dhtHumidity));

    // if (! sgp.IAQmeasure()) {
    //     Serial.println("Measurement failed");
    //     return;
    // }
    // Serial.print("TVOC "); Serial.print(sgp.TVOC); Serial.print(" ppb\t");
    // Serial.print("eCO2 "); Serial.print(sgp.eCO2); Serial.println(" ppm");

    // if (! sgp.IAQmeasureRaw()) {
    //     Serial.println("Raw Measurement failed");
    //     return;
    // }
    // Serial.print("Raw H2 "); Serial.print(sgp.rawH2); Serial.print(" \t");
    // Serial.print("Raw Ethanol "); Serial.print(sgp.rawEthanol); Serial.println("");
    
    // delay(1000);

    // counter++;
    // if (counter == 30) {
    //     counter = 0;

    //     uint16_t TVOC_base, eCO2_base;
    //     if (! sgp.getIAQBaseline(&eCO2_base, &TVOC_base)) {
    //     Serial.println("Failed to get baseline readings");
    //     return;
    //     }
    //     Serial.print("****Baseline values: eCO2: 0x"); Serial.print(eCO2_base, HEX);
    //     Serial.print(" & TVOC: 0x"); Serial.println(TVOC_base, HEX);
    // }

    lightData = analogRead(A0);

    StaticJsonDocument<200> doc;
    doc["formaldehyde"] = formaldehydeData;
    doc["temperature"] = temperatureData;
    doc["humditiy"] = humidityData;
    doc["light"] = lightData;
        
    serializeJson(doc, resultJson);

//    Serial.print(resultJson.length());
//    Serial.print("\r\n\r\n");

    Serial.print(resultJson);
    Serial.print("\n");
    
    resultJson.remove(0);
}
