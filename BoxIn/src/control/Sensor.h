#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Adafruit_AHTX0.h>
#include <Adafruit_ADS1X15.h>
#include <DHT.h>
#include "INA219.h"

#define BATT_LOW_LEVEL 2.5
#define BATT_HIGH_LEVEL 4.2
#define BATT_PERCENT_LOW 0.0
#define BATT_PERCENT_HIGH 100.0
#define luxSensor 0x23
#define DHTPIN 15
#define DHTTYPE DHT22
#define DRY_MILLIVOLT 1980 // ค่าเอ้าต์พุท เมื่อทดสอบที่อากาศแห้ง
#define WET_MILLIVOLT 1387 // ค่าเอ้าต์พุท เมื่อทดสอบน้ำเซนเซอร์จุ่มน้ำทั้งตัว

float t_in_a, h_in_a, t_in_b, h_in_b, Lux, batt, battPercent;
int h_in_s;
// int cycleRead;
Adafruit_AHTX0 aht;
sensors_event_t humidity, temp;
Adafruit_ADS1115 humiditySoil;

uint8_t buf[4] = {0};
DHT dht(DHTPIN, DHTTYPE);
INA219 sensorBatt(0x40);

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

void readTempInAir()
{
    if (!aht.begin())
    {
        // Serial.println("Could not find AHT? Check wiring");
        t_in_a = -1;
        h_in_a = -1;
    }
    else
    {
        aht.getEvent(&humidity, &temp); // วัดค่าอุณหภูมิและความชื้น
        t_in_a = temp.temperature;
        h_in_a = humidity.relative_humidity;
    }
}

void readHumiInSoil()
{
    if (!humiditySoil.begin())
    {
        // Serial.println("Failed to initialize ADS.");
        h_in_s = -1;
    }
    else
    {
        int16_t sensorValue;
        sensorValue = humiditySoil.readADC_SingleEnded(0) / 10;
        h_in_s = map(sensorValue, DRY_MILLIVOLT, WET_MILLIVOLT, 0, 100);
        Serial.print("sensorValue : ");
        Serial.println(sensorValue);
        Serial.print("Humidity : ");
        Serial.println(h_in_s);
        if (h_in_s < 0)
        {
            h_in_s = 0;
        }
        else if (h_in_s > 100)
        {
            h_in_s = 100;
        }
    }
}

uint8_t readRegister(uint8_t reg, const void *pBuf, size_t size)
{
    if (pBuf == NULL)
    {
        // Serial.println("pBuf ERROR!! : null pointer");
    }
    uint8_t *_pBuf = (uint8_t *)pBuf;
    Wire.beginTransmission(luxSensor);
    Wire.write(&reg, 1);
    if (Wire.endTransmission() != 0)
    {
        return 0;
    }
    Wire.requestFrom(luxSensor, size);
    for (uint16_t i = 0; i < size; i++)
    {
        _pBuf[i] = Wire.read();
    }
    return size;
}

void readLight()
{
    int checkLightsensor = readRegister(0x10, buf, 2); // Register Address 0x10
    if (checkLightsensor == 0)
    {
        Serial.println("ไม่พบเซนเซอร์แสง");
        Lux = -1;
    }
    else
    {
        uint16_t data = buf[0] << 8 | buf[1];
        Lux = (((float)data) / 1.2);
    }
}

void readTempInBox()
{
    h_in_b = dht.readHumidity();
    t_in_b = dht.readTemperature();

    if (isnan(h_in_b) || isnan(t_in_b))
    {
        Serial.println(F("Failed to read from DHT sensor!"));
        h_in_b = -1;
        t_in_b = -1;
        return;
    }
}

String readSensorAll()
{
    readTempInAir();
    readHumiInSoil();
    readLight();
    readTempInBox();
    readBatt();
    return String(t_in_b) + "," + String(t_in_a) + "," + String(h_in_a) + "," + String(h_in_b) + "," + String(h_in_s) + "," + String(Lux) + "," + String(batt);
}