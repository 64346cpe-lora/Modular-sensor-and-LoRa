#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Adafruit_AHTX0.h>
#include <Adafruit_ADS1X15.h>
#include <DHT.h>
#include "INA219.h"
#include <DFRobot_ESP_EC.h>
#include <DFRobot_ESP_PH_WITH_ADC.h>

#define BATT_LOW_LEVEL 2.5
#define BATT_HIGH_LEVEL 4.2
#define BATT_PERCENT_LOW 0
#define BATT_PERCENT_HIGH 100
#define luxSensor 0x23
#define DHTPIN 15
#define DHTTYPE DHT22
int btnState = 0;
float t_in_b, h_in_b, batt, ecVoltage, ecValue, phVoltage, phValue, temperature = 25, pumpVoltage, battPercent;

// int cycleRead;
bool statusPump;
DFRobot_ESP_EC EC;
DFRobot_ESP_PH_WITH_ADC PH;
Adafruit_AHTX0 aht;
sensors_event_t humidity, temp;
Adafruit_ADS1115 ecSensor;
Adafruit_ADS1115 pHSensor;
Adafruit_ADS1115 nonContactWater;

uint8_t buf[4] = {0};
DHT dht(DHTPIN, DHTTYPE);
INA219 sensorBatt(0x40);

void setupWaterSensor()
{
    Serial.begin(115200);
    ecSensor.setGain(GAIN_ONE);
    pHSensor.setGain(GAIN_ONE);
    nonContactWater.setGain(GAIN_ONE);
    // ecSensor.begin(0x48);
    // pHSensor.begin(0x49);
    EC.begin();
    PH.begin();
}

void readBatt()
{
    if (!sensorBatt.begin())
    {
        Serial.println("could not connect INA219. Fix and Reboot");
        batt = 0;
        battPercent = 0;
    }
    else
    {
        sensorBatt.setMaxCurrentShunt(5, 0.002);
        batt = sensorBatt.getBusVoltage();
        battPercent = ((batt - BATT_LOW_LEVEL) * (BATT_PERCENT_HIGH - BATT_PERCENT_LOW)) / (BATT_HIGH_LEVEL - BATT_LOW_LEVEL) + BATT_PERCENT_LOW;
        // battPercent = map(batt, BATT_LOW_LEVEL, BATT_HIGH_LEVEL, BATT_PERCENT_LOW, BATT_PERCENT_HIGH);
    }
    if (battPercent < 0)
    {
        battPercent = 0;
    }
    else if (battPercent > 100)
    {
        battPercent = 100;
    }
}

void readEcSensor()
{
    if (!ecSensor.begin(0x49))
    {
        Serial.println("Failed to initialize ecSensor.");
        ecValue = -1;
    }
    else
    {
        ecVoltage = ecSensor.readADC_SingleEnded(3) / 10;
        ecValue = EC.readEC(ecVoltage, temperature);
        if (ecValue < 0)
        {
            ecValue = 0;
        }
    }
}

void readPhSensor()
{
    if (!pHSensor.begin(0x4A))
    {
        Serial.println("Failed to initialize pHSensor.");
        phValue = -1;
    }
    else
    {
        phVoltage = pHSensor.readADC_SingleEnded(3) / 10;
        phValue = PH.readPH(phVoltage, temperature);
        if (phValue < 0)
        {
            phValue = 0;
        }
    }
}

void readStatusPump()
{
    if (!nonContactWater.begin(0x48))
    {
        Serial.println("Failed to initialize nonContactWater.");
        statusPump = 0;
    }
    else
    {
        pumpVoltage = nonContactWater.readADC_SingleEnded(3);
        if (pumpVoltage >= 100)
        {
            statusPump = 1;
        }
        else
        {
            statusPump = 0;
        }
    }
}

void readTempInBox()
{
    h_in_b = dht.readHumidity();
    t_in_b = dht.readTemperature();

    if (isnan(h_in_b) || isnan(t_in_b))
    {
        Serial.println(F("Failed to read from DHT sensor!"));
        h_in_b = 0;
        t_in_b = 0;
        return;
    }
}

String readSensorAll()
{
    readBatt();
    // Serial.println("readBatt success");
    readTempInBox();
    // Serial.println("readTempInBox success");
    setupWaterSensor();
    // Serial.println("setupWaterSensor success");
    // readWaterSensor();
    // Serial.println("readWaterSensor success");
    readEcSensor();
    readPhSensor();
    readStatusPump();
    Serial.print("pumpVoltage");
    Serial.println(pumpVoltage);
    Serial.print("statusPump");
    Serial.println(statusPump);
    return String(t_in_b) + "," + String(h_in_b) + "," + String(ecValue) + "," + String(phValue) + "," + String(statusPump) + "," + String(batt);
    // return String(t_in_b) + "," + String(h_in_b) + "," + String(ecValue) + "," + String(phValue) + ",1," + String(batt);
}