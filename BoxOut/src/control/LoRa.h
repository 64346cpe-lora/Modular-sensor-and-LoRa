#include <Arduino.h>
#include <LoRa.h>

#ifndef LoRa
#define SCK 5
#define MISO 19
#define MOSI 27
#define SS 18
#define RST 14
#define DIO0 26
#define BAND 923E6
#endif

#define ADDR_SOUCE 0xBA
#define ADDR_DEST 0xFF

unsigned long loraTime = 0;
unsigned long timeWorkingPump = 0;

void initLoRa()
{
    SPI.begin(SCK, MISO, MOSI, SS);
    LoRa.setPins(SS, RST, DIO0);
    while (!LoRa.begin(BAND))
    {
        Serial.println("Starting LoRa failed!");
        delay(500);
    }
    Serial.println("LoRa Initializing OK!");
    LoRa.setTxPower(18);
}

int checkDataLoRa()
{
    int lenghtData = 6;
    String loraData[lenghtData];
    String receiveData;
    int startIndex = 0;
    int endIndex = 0;
    int i = 0;
    while (LoRa.available())
    {
        receiveData = LoRa.readString();
        Serial.print("Receive : ");
        Serial.println(receiveData);
    }

    // print RSSI of packet
    int rssi = LoRa.packetRssi();
    int snr = LoRa.packetSnr();
    Serial.print("Data RSSI : ");
    Serial.println(rssi);
    Serial.print("Data SNR : ");
    Serial.println(snr);

    for (int i = 0; i < lenghtData; i++)
    {
        endIndex = receiveData.indexOf(',', startIndex);
        if (endIndex == -1)
        {
            endIndex = receiveData.length();
        }
        loraData[i] = receiveData.substring(startIndex, endIndex);
        startIndex = endIndex + 1;
    }
    // Serial.print("loraData[0]");
    // Serial.println(loraData[0]);
    // Serial.print("loraData[1]");
    // Serial.println(loraData[1]);
    // Serial.print("loraData[2]");
    // Serial.println(loraData[2]);
    // return true;

    if (loraData[0].equals(String(ADDR_DEST, DEC)) && loraData[1].equals(String(ADDR_SOUCE, DEC)) && loraData[2].equals("0")) // Addr true and data is true
    {
    /*
    loraData[0] : address gateway 
    loraData[1] : address end-device
    loraData[2] : status LoRa
                  status LoRa value = 0 is data correct
                  status LoRa value = 1 is data not correct
    loraData[3] : hard reset
    loraData[4] : status pump
    loraData[5] : pump working time
    */
        if (loraData[3].equals("1")) // Hard reset == 1
        {
            return 10;
        }
        else // Hard reset == 0
        {
            int pumpState = loraData[4].toInt();
            Serial.print("loraData[4]");
            Serial.println(loraData[4].toInt());
            switch (pumpState)
            {
            case 0:
                return 0; // case 0 : data correct
            case 1:
                timeWorkingPump = loraData[5].toInt();
                return 1; // case 1 : data correct ปั๊มทำงานตามเวลา
            case 2:
                return 2; // case 2 : data correct ปั๊มทำงานตามความชื้น
            case 3:
                return 3; // case 3 : data correct ปั๊มทำงานจากการสั่งบนเว็บ
            case 4:
                return 4;// case 4 : data correct ปั๊มหยุดทำงาน
            }
        }
    }
    return 11;
}

int receiveLoRa()
{
    int packetSize = LoRa.parsePacket();
    return packetSize;
}

void sentLoRa(String LoRaData)
{
    // Serial.println("This is fanction sentLoRa!!");
    LoRa.beginPacket();
    Serial.println("LoRa sent");
    // LoRaData = String(t_in_a) + "," + String(h_in_a);
    LoRa.write(ADDR_SOUCE);
    LoRa.write(ADDR_DEST);
    // LoRa.write(LoRaData.length());
    LoRa.print(LoRaData);
    LoRa.endPacket();
    Serial.print("LoRa packet sent. : ");
    String LoRaDataTest = String(ADDR_SOUCE) + String(ADDR_DEST) + LoRaData;
    Serial.println(LoRaDataTest);
    LoRaData = "";
    // onReceive();
}