#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);

int lcdState = 0;

void lcdInit()
{
    lcd.display(); // เปิดการแสดงตัวอักษร
    lcd.backlight();
    lcd.clear();
}

void lcdPrintLine()
{
    lcd.setCursor(0, 0);
    lcd.print("--------------------");
    lcd.setCursor(0, 3);
    lcd.print("--------------------");
}

void lcdActive()
{
    Serial.println("lcdActive");
    lcdInit();
    lcd.setCursor(0, 0);
    lcd.print("Please wait");
    // Serial.println("LCD Active please wait");
}

void lcdShutdown()
{
    lcd.clear();
    lcd.noDisplay();
    lcd.noBacklight();
}

void showMode(bool mode)
{
    lcdInit();
    lcdPrintLine();
    lcd.setCursor(0, 1);
    lcd.print("     Mode LoRa      ");
    lcd.setCursor(0, 2);
    if (mode)
    {
        lcd.print("     Debug Mode     ");
    }
    else
    {
        lcd.print("    Normal Mode     ");
    }
}

void lcdFirstPage(float batt, float lux, float temp, float humi)
{
    Serial.print("in Display : ");
    Serial.print("t_in_b : ");
    Serial.println(temp);
    Serial.print("h_in_b : ");
    Serial.println(humi);
    lcdInit();
    Serial.println("lcdFirstPage");
    lcd.setCursor(0, 0);
    lcd.print("Batterry :");
    lcd.setCursor(11, 0);
    lcd.print(batt);
    lcd.setCursor(0, 1);
    lcd.print("Lux      :");
    lcd.setCursor(11, 1);
    if (lux == -1)
    {
        lcd.print("No Data");
    }
    else
    {
        lcd.print(lux);
    }
    lcd.setCursor(0, 2);
    lcd.print("T in Box :");
    lcd.setCursor(11, 2);
    if (temp == -1)
    {
        lcd.print("No Data");
    }
    else
    {
        lcd.print(temp);
    }
    lcd.setCursor(0, 3);
    lcd.print("H in Box :");
    lcd.setCursor(11, 3);
    if (humi == -1)
    {
        lcd.print("No Data");
    }
    else
    {
        lcd.print(humi);
    }
}

void lcdSecondPage(float tempA, float humiA, float humiS)
{
    lcdInit();
    Serial.println("lcdSecondPage");
    lcd.setCursor(0, 0);
    lcd.print("T in Air :");
    lcd.setCursor(11, 0);
    if (tempA == -1)
    {
        lcd.print("No Data");
    }
    else
    {
        lcd.print(tempA);
    }
    lcd.setCursor(0, 1);
    lcd.print("H in Air :");
    lcd.setCursor(11, 1);
    if (humiA == -1)
    {
        lcd.print("No Data");
    }
    else
    {
        lcd.print(humiA);
    }
    lcd.setCursor(0, 2);
    lcd.print("H in Sol :");
    lcd.setCursor(11, 2);
    if (humiS == -1)
    {
        lcd.print("No Data");
    }
    else
    {
        lcd.print(humiS);
    }
}

void sentDataPage(int timeToSent)
{
    lcd.noBacklight();
    lcd.display();
    lcd.clear();
    lcdPrintLine();
    lcd.setCursor(0, 1);
    lcd.print("Sent data to gateway");
    lcd.setCursor(0, 2);
    if (timeToSent == 0)
    {
        lcd.print("      1st time     ");
    }
    else if (timeToSent == 1)
    {
        lcd.print("      2nd time      ");
    }
    else if (timeToSent == 2)
    {
        lcd.print("      3rd time      ");
    }
    else if (timeToSent == 3)
    {
        lcd.print("      4th time      ");
    }
    else
    {
        lcd.print("      5th time      ");
    }
}

void waitData(bool statusLCD)
{
    if (statusLCD)
    {
        lcd.backlight();
    }
    else
    {
        lcd.noBacklight();
    }

    lcd.setCursor(0, 1);
    lcd.print("  Status send data  ");
    lcd.setCursor(0, 2);
    lcd.print("Waiting receive data");
}

void receivePage(bool statusLoRa)
{
    lcd.display();
    lcd.clear();
    lcdPrintLine();
    lcd.setCursor(0, 1);
    lcd.print("  Status send data  ");
    lcd.setCursor(0, 2);
    if (statusLoRa)
    {
        lcd.print(" LoRa send success  ");
    }
    else
    {
        lcd.print("   LoRa send fail   ");
    }
}

void lcdPressedBTN(int num)
{
    lcdInit();
    lcdPrintLine();
    lcd.setCursor(0, 1);
    lcd.print("    Time pressed    ");
    lcd.setCursor(10, 2);
    lcd.print(num);
}

void sleepPage(int num, bool statusData)
{
    lcdPrintLine();
    lcd.setCursor(0, 1);
    if (statusData)
    {
        lcd.print(" LoRa send success  ");
    }
    else
    {
        lcd.print("   LoRa send fail   ");
    }
    lcd.setCursor(0, 2);
    lcd.print("Box sensor Sleep : ");
    lcd.setCursor(19, 2);
    lcd.print(num);
}

void resetPage(int count){
    lcdPrintLine();
    lcd.clear();
    lcd.setCursor(0, 1);
    lcd.print("    BOX in reset   ");
    lcd.setCursor(0,2);
    lcd.print("  pressed wait : ");
    lcd.setCursor(17,2);
    lcd.print(count);
}