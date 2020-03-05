#include <DHT_U.h>
#include <Wire.h>
#include <Adafruit_SGP30.h>
#include <SoftwareSerial.h>
#include <math.h>
#include <ArduinoJson.h>
#define DHTPIN 4
#define DHTTYPE DHT11
#define RX 2
#define TX 3
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
int32_t temperatureData, humidityData, eco2Data, tvocData, formaldehydeData, lightData;
String resultJson;
int counter = 0;

uint32_t getAbsoluteHumidity(float temperature, float humidity)
{
    const float absoluteHumidity = 216.7f * ((humidity / 100.0f) * 6.112f * exp((17.62f * temperature) / (243.12f + temperature)) / (273.15f + temperature)); // [g/m^3]
    const uint32_t absoluteHumidityScaled = static_cast<uint32_t>(1000.0f * absoluteHumidity);                                                                // [mg/m^3]
    return absoluteHumidityScaled;
}

void setup()
{
    Serial.begin(9600);
    serialSensor.begin(9600);
    dht.begin();
    sgp.begin();
    if (!sgp.begin())
    {
        Serial.println("SGP sensor not found :(");
    }
}

void loop()
{
    delay(2000);
    //DART Start
    if (serialSensor.available() > 0)
    {
        serialSensor.readBytes(serialIn, serialSensor.available());
        for (size_t i = 1; i <= 7; i++)
        {
            hchoSum += serialIn[i];
        }
        if (serialIn[0] == 0xFF && serialIn[8] == byte(~(hchoSum) + 1))
        {
            hchoHightNum = serialIn[4];
            hchoLowNum = serialIn[5];
            formaldehydeData = hchoHightNum * 256 + hchoLowNum;
            if (formaldehydeData > 2000)
            {
                formaldehydeData = -1;
            }
        }
        else
        {
            formaldehydeData = -1;
        }
    }
    else
    {
        formaldehydeData = -1;
    }

    hchoSum = 0;

    // Get temperature event and print its value.
    sensors_event_t dhtEvent;
    dht.temperature().getEvent(&dhtEvent);
    if (isnan(dhtEvent.temperature))
    {
        temperatureData = -1;
    }
    else
    {
        dhtTemperature = dhtEvent.temperature; // [°C]
        temperatureData = floor(dhtTemperature);
    }
    // Get humidity event and print its value.
    dht.humidity().getEvent(&dhtEvent);
    if (isnan(dhtEvent.relative_humidity))
    {
        //Serial.println(F("Error reading humidity!"));
        humidityData = -1;
    }
    else
    {
        dhtHumidity = dhtEvent.relative_humidity; // [%RH]
        humidityData = floor(dhtHumidity);
    }

    //SGP Start
    float temperature = dhtTemperature; // [°C]
    float humidity = dhtHumidity;       // [%RH]
    sgp.setHumidity(getAbsoluteHumidity(dhtTemperature, dhtHumidity));

    if (!sgp.IAQmeasure())
    {
        // Serial.println("Measurement failed");
        eco2Data = -1;
        tvocData = -1;
    }
    else
    {
        eco2Data = sgp.eCO2; // [ppm]
        tvocData = sgp.TVOC; // [ppb]
    }
    counter++;
    if (counter == 15)
    {
        counter = 0;
        uint16_t TVOC_base, eCO2_base;
        sgp.getIAQBaseline(&eCO2_base, &TVOC_base);
    }
    lightData = analogRead(A0);

    StaticJsonDocument<200> doc;
    doc["temperature"] = temperatureData;
    doc["humditiy"] = humidityData;
    doc["eco2"] = eco2Data;
    doc["formaldehyde"] = formaldehydeData;
    doc["tvoc"] = tvocData;
    doc["light"] = lightData;

    serializeJson(doc, resultJson);
    Serial.print(resultJson);
    Serial.print("\n");
    resultJson.remove(0);
}
