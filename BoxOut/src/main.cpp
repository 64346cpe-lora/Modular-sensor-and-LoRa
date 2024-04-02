#include <Arduino.h>
#include <EEPROM.h>
#include <EasyButton.h>
#include "control/LoRa.h"
#include "control/Sensor.h"
#include "control/Display.h"

#define BTN_ACTIVE_LCD 25
#define BTN_CHANGE_MODE 32
#define BTN_ACTIVE_AC 33
#define RELAY 2
#define GPIO_LCD GPIO_NUM_25
#define MODE_GPIO 0x302000000
#define SW_DEBOUNCE_TIME 400
#define PRESSED_RESET_TIME 5000
#define LCD_WORKING_TIME 30000
#define LCD_DEBUG_TIME 5000
#define TIME_WAIT_INPUT_CMD 5000
#define PERIOD_INTERVAL 1000
#define ADDR_MODE 0x70

EasyButton buttonLCD(BTN_ACTIVE_LCD);
EasyButton buttonMode(BTN_CHANGE_MODE);
EasyButton buttonAC(BTN_ACTIVE_AC);

int debugMode = 0;
hw_timer_t *timer = NULL;
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;

int state = 1;

int periodSentData = 0;
int statusSentData;
boolean statusLCD = false;
boolean lcdFlag = false;
boolean statusAC = false;
boolean calibrationIsRunning = false;
boolean isBTNDebugPressed = false;
char cmd[10];
String sensorData = "";
unsigned long btnLcdPressed = 0;
unsigned long btnModePressed = 0;
unsigned long btnAcPressed = 0;
unsigned long previousMillisSw = 0;
unsigned long timeToPressedBTN = 0;
unsigned long timeToDebugLCD = 0;
unsigned long timeToActiveLCD = 0;
unsigned long timeToPumpActive = 0;
unsigned long timeReadSensor = 0;
unsigned long lastTimeInterval = 0;
unsigned long stateFive = 0;
unsigned long checkPressedOneSec = 0;
unsigned long previousMillisCheckPump = 0;

int i = 0;
bool readSerial(char result[])
{
    while (Serial.available() > 0)
    {
        char inChar = Serial.read();
        if (inChar == '\n')
        {
            result[i] = '\0';
            Serial.flush();
            i = 0;
            return true;
        }
        if (inChar != '\r')
        {
            result[i] = inChar;
            i++;
        }
        delay(1);
    }
    return false;
}

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

void setMode(int mode)
{
    if (mode == 0)
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
    timeToDebugLCD = millis();
    statusLCD = true;
    Serial.println("Change mode");
    if (debugMode)
        debugMode = 0;
    else
        debugMode = 255;
    setMode(debugMode);
    Serial.println(debugMode);
    timeToActiveLCD = millis();
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
    timerAlarmWrite(timer, 5000000, true);             // Set period to 5 second (5,000,000 microseconds)
    timerAlarmEnable(timer);                           // Enable the timer
}

void showDisplay()
{
    sensorData = readSensorAll();
    if (lcdState == 0 || lcdState == 1)
    {
        timeToActiveLCD = millis();
        lcdState = 2;
        lcdFirstPage(battPercent, t_in_b, h_in_b);
    }
    else if (lcdState == 2)
    {
        timeToActiveLCD = millis();
        lcdState = 1;
        lcdSecondPage(ecValue, phValue);
    }
}

void setPumpWorking(boolean status)
{
    statusAC = status;
    Serial.print("setPumpWorking");
    Serial.println(status);
    digitalWrite(RELAY, status);
    Serial.println(RELAY);
}

void toggleAC()
{
    isBTNDebugPressed = false;
    statusAC = !statusAC;
    setPumpWorking(statusAC);
    state = 1;
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
    case 33:
        Serial.println("Wakeup by GPIO33");
        Serial.print("Active AC");
        toggleAC();
        break;
    default:
        Serial.print("ESP32 wake up in another cause!!!!");
    }
}

void setTimerPump()
{
    timeWorkingPump = timeWorkingPump * 60 * 1000;
}

void btnLcdOnPressed()
{
    checkPressedOneSec = millis();
    timeToPressedBTN = millis();
    isBTNDebugPressed = false;
    statusLCD = true;
    int count = 0;
    while (digitalRead(BTN_ACTIVE_LCD) != 0)
    {
        // Serial.println("Pressed");
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
    }
    sensorData = readSensorAll();
    Serial.println(sensorData);
    Serial.println(lcdState);
    if (lcdState == 0)
    {
        timeToActiveLCD = millis();
        lcdState = 1;
        showDisplay();
        enableTimeInterrupt();
    }
    else
    {
        timeToActiveLCD = millis();
        showDisplay();
    }
}

void setup()
{
    EEPROM.begin(512);
    Serial.begin(115200);
    //  EEPROM.put(ADDR_MODE, 0);
    //  EEPROM.commit();
    initLoRa();
    Serial.println("LoRa init");
    lcd.init();
    Serial.println("lcd init");
    dht.begin();
    Serial.println("dht init");
    pinMode(BTN_ACTIVE_LCD, INPUT);
    pinMode(BTN_CHANGE_MODE, INPUT);
    pinMode(BTN_ACTIVE_AC, INPUT);
    pinMode(RELAY, OUTPUT);

    esp_sleep_enable_ext1_wakeup(MODE_GPIO, ESP_EXT1_WAKEUP_ANY_HIGH);
    checkWakeupReason();

    Serial.println("Curren mode : ");
    getConfigMode();
    Serial.println(debugMode);
    setMode(debugMode);
    Serial.println("ESP Active");
    buttonLCD.onPressed(btnLcdOnPressed);
    buttonMode.onPressed(changeMode);
    buttonAC.onPressed(toggleAC);
}

void loop()
{
    buttonLCD.read();
    buttonMode.read();
    buttonAC.read();
    if (lcdFlag) // Change the screen every time. When function changeDisplay works.
    {
        sensorData = readSensorAll();
        if (lcdState == 1)
        {
            lcdState = 2;
            lcdFlag = false;
            lcdFirstPage(battPercent, t_in_b, t_in_b);
        }
        else
        {
            lcdState = 1;
            lcdFlag = false;
            lcdSecondPage(ecValue, phValue);
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

    if (state == 1) // Read sensor all
    {
        sensorData = readSensorAll();
        Serial.print("state : ");
        Serial.println(state);
        state++;
    }
    if (state == 2) // Sent data to geteway
    {
        Serial.print("state : ");
        Serial.println(state);
        sentLoRa(sensorData + "," + statusAC);
        if (!statusLCD)
        {
            sentDataPage(periodSentData);
        }
        state++;
    }
    if (state == 3) // Receive data from gateway
    {
        if (statusAC)
        {
            pumpActive();
        }
        int packetSize = LoRa.parsePacket();
        Serial.print("state : ");
        Serial.println(state);
        loraTime = millis();
        while (true)
        {
            buttonLCD.read();
            buttonMode.read();
            buttonAC.read();
            // waitDataInLoop();
            packetSize = LoRa.parsePacket();
            if (millis() - timeToPumpActive >= timeWorkingPump && timeWorkingPump != 0)
            {
                Serial.println(timeWorkingPump);
                setPumpWorking(LOW);
                lcdShutdown();
                timeWorkingPump = 0;
                state = 4;
                timeReadSensor = millis();
                sensorData = readSensorAll();
                delay(1000);
                sentLoRa(sensorData + "," + statusAC);
                break;
            }
            else if (packetSize) // ESP32 have receives data
            {
                Serial.println("packetSize");
                statusSentData = checkDataLoRa();
                Serial.print("statusSentData : ");
                Serial.println(statusSentData);
                if (statusSentData == 0 && statusAC == 0)
                {
                    // receivePage(true);
                    Serial.println("LoRa send success");
                    state = 4;
                    timeReadSensor = millis();
                    break;
                }
                else if(statusSentData == 0 && statusAC == 1){
                    Serial.println("LoRa send success but pump working");
                    sensorData = readSensorAll();
                    delay(1000);
                    sentLoRa(sensorData + "," + statusAC);
                    break;
                }
                else if (statusSentData == 1)
                {
                    Serial.println("Set timer pump");
                    setTimerPump();
                    setPumpWorking(HIGH);
                    Serial.print("pump timer : ");
                    Serial.println(timeWorkingPump / 1000);
                    timeToPumpActive = millis();
                    sensorData = readSensorAll();
                    delay(1000);
                    sentLoRa(sensorData + "," + statusAC);
                    break;
                }
                else if (statusSentData == 2)
                {
                    Serial.println("Pump start working. Control by humidity");
                    setPumpWorking(HIGH);
                    sensorData = readSensorAll();
                    delay(1000);
                    sentLoRa(sensorData + "," + statusAC);
                    break;
                }
                else if (statusSentData == 3)
                {
                    Serial.println("Pump start working. Control by blynk");
                    setPumpWorking(HIGH);
                    sensorData = readSensorAll();
                    delay(1000);
                    sentLoRa(sensorData + "," + statusAC);
                    break;
                }
                else if (statusSentData == 4)
                {
                    Serial.println("Pump stop working. Control by blynk");
                    lcdShutdown();
                    setPumpWorking(LOW);
                    state = 1;
                    sensorData = readSensorAll();
                    delay(1000);
                    sentLoRa(sensorData + "," + statusAC);
                    break;
                }
                else if (statusSentData == 10)
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
                        else if (count <= 0)
                        {
                            Serial.println("ESP restart");
                            esp_restart();
                        }
                        else if (millis() - timeWaitReset >= PERIOD_INTERVAL)
                        {
                            timeWaitReset = millis();
                            Serial.println(count);
                            count--;
                            resetPage(count);
                        }
                    }
                }
                else if (statusSentData == 11 && periodSentData < 5 && millis() - loraTime >= 5000)
                {
                    periodSentData++;
                    Serial.print("LoRa sent fail resent : ");
                    Serial.println(periodSentData);
                    state = 2;
                    break;
                }
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
                periodSentData = 0;
                Serial.println("LoRa sent fail");
                state = 4;
                timeReadSensor = millis();
                break;
            }
            else if (state != 3)
            {
                break;
            }
        }
    }

    if (state == 4)
    {
        if (statusAC == 1)
        {
            state = 3;
            periodSentData = 0;
            return;
        }
        // Serial.println(millis() - timeReadSensor);
        if (millis() - timeReadSensor <= TIME_WAIT_INPUT_CMD || calibrationIsRunning)
        {
            if (millis() - lastTimeInterval >= PERIOD_INTERVAL)
            {
                Serial.println("Calibrate ec & pH is not running");
                lastTimeInterval = millis();
                if (calibrationIsRunning)
                {
                    Serial.println(F("[main]...>>>>>> calibration is running, to exit send exitph or exitec through serial <<<<<<"));
                    // EC
                    ecVoltage = ecSensor.readADC_SingleEnded(3) / 10;
                    Serial.print(F("[EC Voltage]... ecVoltage: "));
                    Serial.println(ecVoltage);
                    ecValue = EC.readEC(ecVoltage, temperature); // convert voltage to EC with temperature compensation
                    Serial.print(F("[EC Read]... EC: "));
                    Serial.print(ecValue);
                    Serial.println(F("ms/cm"));
                    // pH
                    phVoltage = pHSensor.readADC_SingleEnded(3) / 10;
                    Serial.print(F("[pH Voltage]... phVoltage: "));
                    Serial.println(phVoltage);
                    phValue = PH.readPH(phVoltage, temperature);
                    Serial.print(F("[pH Read]... pH: "));
                    Serial.println(phValue);
                }
                if (readSerial(cmd))
                {
                    strupr(cmd);

                    if (calibrationIsRunning || strstr(cmd, "PH") || strstr(cmd, "EC"))
                    {
                        calibrationIsRunning = true;
                        Serial.println(F("[]... >>>>>calibration is now running PH and EC are both reading, if you want to stop this process enter EXITPH or EXITEC in Serial Monitor<<<<<"));
                        if (strstr(cmd, "PH"))
                        {
                            PH.calibration(phVoltage, temperature, cmd); // PH calibration process by Serail CMD
                        }
                        if (strstr(cmd, "EC"))
                        {
                            EC.calibration(ecVoltage, temperature, cmd); // EC calibration process by Serail CMD
                        }
                    }
                    if (strstr(cmd, "EXITPH") || strstr(cmd, "EXITEC"))
                    {
                        calibrationIsRunning = false;
                        timeReadSensor = millis();
                    }
                }
            }
        }
        else
        {
            state = 5;
            return;
        }
    }

    if (state == 5 && !statusLCD) // ESP32 sleep
    {
        stateFive = millis();
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
            buttonLCD.read();
            buttonMode.read();
            buttonAC.read();
            if (statusLCD || state != 5) // Button is pressed. Exit loop.
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