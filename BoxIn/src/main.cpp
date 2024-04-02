#include <Arduino.h>
#include <EEPROM.h>
#include "control/LoRa.h"
#include "control/Sensor.h"
#include "control/Display.h"

#define BTN_ACTIVE_LCD 25
#define BTN_CHANGE_MODE 32
#define GPIO_LCD GPIO_NUM_25
#define MODE_GPIO 0x102000000
#define SW_DEBOUNCE_TIME 400
#define PRESSED_RESET_TIME 5000
#define LCD_WORKING_TIME 30000
#define LCD_DEBUG_TIME 5000
#define INTERVAL_WAIT_PUMP 10000
#define PERIOD_INTERVAL 1000
#define FIVE_SECOND 5000
#define ADDR_MODE 0x70

hw_timer_t *timer = NULL;
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;

int state = 1;
int btnState = 0;

int periodSentData = 0;
int statusSentData;
boolean statusLCD = false;
boolean lcdFlag = false;
int debugMode = 0;
boolean statusPump = false;
boolean isBTNDebugPressed = false;
unsigned long btnLcdPressed = 0;
unsigned long btnModePressed = 0;
String sensorData = "";
unsigned long stateFive = 0;
unsigned long timeToPressedBTN = 0;
unsigned long timeToDebugLCD = 0;
unsigned long timeToActiveLCD = 0;
unsigned long timeSendDataWailPump = 0;
unsigned long checkPressedOneSec = 0;

void updateConfigMode(boolean mode)
{
    EEPROM.put(ADDR_MODE, mode);
    EEPROM.commit();
    EEPROM.get(ADDR_MODE, debugMode);
}

void getConfigMode()
{
    EEPROM.get(ADDR_MODE, debugMode);
}

void setMode(boolean mode)
{
    if (!mode)
    {
        esp_sleep_enable_timer_wakeup(10 * 60 * 1000 * 1000);
    }
    else
    {
        esp_sleep_enable_timer_wakeup(10 * 1000 * 1000);
    }
}

void changeMode()
{
    getConfigMode();
    isBTNDebugPressed = true;
    statusLCD = true;
    Serial.println("Change mode");
    if (debugMode)
        debugMode = 0;
    else
        debugMode = 255;
    setMode(debugMode);
    Serial.println(debugMode);
    timeToDebugLCD = millis();
    showMode(debugMode);
    updateConfigMode(debugMode);
}

void changeDisplay()
{
    portENTER_CRITICAL_ISR(&timerMux);
    lcdFlag = true;
    portEXIT_CRITICAL_ISR(&timerMux);
}

void enableTimeInterrupt()
{
    timer = timerBegin(0, 80, true);                   // Timer 0, divider 80
    timerAttachInterrupt(timer, &changeDisplay, true); // Attach callback function
    timerAlarmWrite(timer, 5000000, true);             // Set period to 0.5 second (500,000 microseconds)
    timerAlarmEnable(timer);                           // Enable the timer
}

void showDisplay()
{
    sensorData = readSensorAll();
    Serial.println(sensorData);
    Serial.println("in showDisplay : ");
    Serial.print("t_in_b : ");
    Serial.println(t_in_b);
    Serial.print("h_in_b : ");
    Serial.println(h_in_b);
    if (lcdState == 0 || lcdState == 1)
    {
        timeToActiveLCD = millis();
        lcdState = 2;
        lcdFirstPage(battPercent, Lux, t_in_b, h_in_b);
    }
    else if (lcdState == 2)
    {
        timeToActiveLCD = millis();
        lcdState = 1;
        lcdSecondPage(t_in_a, h_in_a, h_in_s);
    }
}

void checkWakeupReason()
{
    uint64_t GPIO_reason = esp_sleep_get_ext1_wakeup_status();
    uint64_t pin = (log(GPIO_reason)) / log(2);
    switch (pin)
    {
    case 25:
        Serial.println("Wakeup by GPIO25");
        Serial.print("Show LCD");
        timeToActiveLCD = millis();
        statusLCD = true;
        enableTimeInterrupt();
        showDisplay();
        break;
    case 32:
        Serial.println("Wakeup by GPIO32");
        Serial.print("Change mode");
        changeMode();
        break;
    default:
        Serial.print("ESP32 wake up in another cause!!!!");
    }
}

IRAM_ATTR void btnActiveLcdIsPressed()
{
    if (millis() - btnLcdPressed >= SW_DEBOUNCE_TIME)
    {
        btnState = 11;
        timeToPressedBTN = millis();
    }
    btnLcdPressed = millis();
}

IRAM_ATTR void btnChangeModeIsPressed()
{
    if (millis() - btnLcdPressed >= SW_DEBOUNCE_TIME)
    {
        // statusSentData = false;
        btnState = 12;
        // Serial.println("btn lcd is pressed");
    }
    btnLcdPressed = millis();
}

void setup()
{
    EEPROM.begin(512);
    Serial.begin(115200);
    // uncomment 172,173 to upload code first time.
    //  EEPROM.put(ADDR_MODE, 0);
    //  EEPROM.commit();
    initLoRa();
    lcd.init();
    dht.begin();
    humiditySoil.setGain(GAIN_ONE);
    pinMode(BTN_ACTIVE_LCD, INPUT);
    pinMode(BTN_CHANGE_MODE, INPUT);

    attachInterrupt(digitalPinToInterrupt(BTN_ACTIVE_LCD), btnActiveLcdIsPressed, RISING);
    attachInterrupt(digitalPinToInterrupt(BTN_CHANGE_MODE), btnChangeModeIsPressed, RISING);
    esp_sleep_enable_ext1_wakeup(MODE_GPIO, ESP_EXT1_WAKEUP_ANY_HIGH);
    checkWakeupReason();

    Serial.println("Curren mode : ");
    getConfigMode();
    Serial.println(debugMode);
    setMode(debugMode);
    Serial.println("ESP Active");
}

void loop()
{
    if (lcdFlag) // Change the screen every time. When function changeDisplay works.
    {
        sensorData = readSensorAll();
        if (lcdState == 1)
        {
            lcdState = 2;
            lcdFirstPage(battPercent, Lux, t_in_b, h_in_b);
            lcdFlag = false;
        }
        else
        {
            lcdState = 1;
            lcdSecondPage(t_in_a, h_in_a, h_in_s);
            lcdFlag = false;
        }
    }
    if (millis() - timeToDebugLCD >= LCD_DEBUG_TIME && statusLCD && timeToDebugLCD != 0)
    {
        Serial.println("lcd off");
        statusLCD = false;
        lcdShutdown();
    }
    
    if (millis() - timeToActiveLCD >= LCD_WORKING_TIME && statusLCD) // Control screen to turn off.
    {
        Serial.println("lcd off");
        statusLCD = false;
        lcdShutdown();
        // timerAlarmDisable(timer);
    }
    if (btnState == 11) // Pressed button GPIO25
    {
        checkPressedOneSec = millis();
        isBTNDebugPressed = false;
        statusLCD = true;
        int count = 0;
        while (digitalRead(BTN_ACTIVE_LCD) != 0)
        {
            Serial.println("Pressed");
            if (count >= 5)
            {
                Serial.println("Reset ESP");
                esp_restart();
            }
            if (millis() - checkPressedOneSec >= PERIOD_INTERVAL)
            {
                checkPressedOneSec = millis();
                count++;
                lcdPressedBTN(count);
            }
            // Serial.println(digitalRead(BTN_ACTIVE_LCD));
        }
        sensorData = readSensorAll();
        if (lcdState == 0)
        {
            timeToActiveLCD = millis();
            // lcdActive();
            lcdState = 1;
            showDisplay();
            enableTimeInterrupt();
        }
        else
        {
            timeToActiveLCD = millis();
            showDisplay();
        }
        btnState = 0;
    }
    if (btnState == 12) // Pressed button GPIO35
    {
        changeMode();
        btnState = 0;
    }
    if (state == 1) // Read sensor all
    {
        sensorData = readSensorAll();
        Serial.print("state : ");
        Serial.println(state);
        // Serial.println(sensorData);
        state++;
    }
    if (state == 2) // Sent data to geteway
    {
        Serial.print("state : ");
        Serial.println(state);
        sentLoRa(sensorData);
        if (!statusLCD)
        {
            Serial.println(periodSentData);
            sentDataPage(periodSentData);
        }
        state++;
    }
    if (state == 3) // Receive data from gateway
    {
        Serial.print("state : ");
        Serial.println(state);
        loraTime = millis();
        while (true)
        {
            int packetSize = LoRa.parsePacket();
            if (packetSize) // ESP32 have receives data
            {
                Serial.println("Status sent data");
                statusSentData = checkDataLoRa();
                if (statusSentData == 0) // data correct
                {
                    // receivePage(true, statusLCD);
                    Serial.println("LoRa sent success");
                    state = 4;
                    stateFive = millis();
                    break;
                }
                else if (statusSentData == 2)
                {
                    Serial.println("Pump working please wait");
                    // state = 1;
                    statusPump = true;
                    timeSendDataWailPump = millis();
                    break;
                }

                else if (statusSentData == 3) // Hard reset from wweb server.
                {
                    Serial.println("reset from web");
                    int count = 5;
                    unsigned long timeWaitReset = millis();
                    resetPage(count);
                    while (true)
                    {
                        if (btnState == 11 || btnState == 12) // Button is pressed. Exit loop.
                        {
                            break;
                        }
                        else if (count <= 0){
                            Serial.println("ESP restart");
                            esp_restart();
                        }
                        else if (millis() - timeWaitReset >= PERIOD_INTERVAL){
                            timeWaitReset = millis();
                            Serial.println(count);
                            count--;
                            resetPage(count);
                        }
                    }
                }
            }

            else if (millis() - timeSendDataWailPump >= INTERVAL_WAIT_PUMP && statusPump)
            {
                statusPump = false;
                periodSentData = 0;
                Serial.println("Pump working please wait");
                state = 1;
                timeSendDataWailPump = millis();
                break;
            }

            else if (millis() - loraTime >= 5000 && (statusSentData == 0 || statusSentData == 11)) // Data not received within 5 seconds. Send again.
            {
                periodSentData++;
                Serial.print("LoRa sent fail resent : ");
                Serial.println(periodSentData);
                state = 2;
                break;
            }
            else if (millis() - loraTime >= 10000)
            {
                Serial.print("LoRa sent again");
                state = 2;
                break;
            }
            else if (periodSentData >= 5) // Data not received within 25 seconds. Send fail.
            {
                // receivePage(false, statusLCD);
                Serial.println("LoRa sent fail");
                state = 4;
                stateFive = millis();
                break;
            }
            else if (btnState == 11 || btnState == 12) // Button is pressed. Exit loop.
            {
                break;
            }
        }
    }
    if (state == 4 && !statusLCD) // ESP32 sleep
    {
        bool statusData;
        int count = 5;
        if (periodSentData >= 5)
        {
            statusData = false;
            receivePage(false);
        }
        else if (statusSentData == 0)
        {
            statusData = true;
            receivePage(true);
        }
        while (true)
        {
            if (btnState == 11 || btnState == 12) // Button is pressed. Exit loop.
            {
                break;
            }
            if (millis() - stateFive >= PERIOD_INTERVAL)
            {
                stateFive = millis();
                sleepPage(count, statusData);
                count--;
                Serial.println(count);
            }
            if (count < 0)
            {
                lcdShutdown();
                Serial.print("state : ");
                Serial.println(state);
                Serial.println("ESP Sleep");
                updateConfigMode(debugMode);
                Serial.println(debugMode);
                esp_deep_sleep_start();
            }
        }
    }
}