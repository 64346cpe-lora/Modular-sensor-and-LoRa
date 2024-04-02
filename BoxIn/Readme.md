## -------------------V1.1 beta---------------------- <br>
# main <br>
Read Sensor <br>
Send data to gateway box <br>
Receive data from gateway <br>
ESP32 sleep

# GPIO 25 connect switch
Pressed for show LCD <br>
lcd state 0 for function activeLCD <br>
lcd state 1 for function lcdFirstPage <br>
lcd state 2 for function lcdSecondPage <br>
support interrupt <br>
support pressed BTN to active lcd when ESP32 sleep <br>

# GPIO 35 connect switch <br>
Pressed for change mode <br>
mode '0' normol send data every 2 min. <br>
mode '1' debug send data every 10 sec. <br>
support interrupt <br>
support pressed BTN to change mode when ESP32 sleep <br>

# LCD in front <br>
change lcd every 5 sec <br>
lcd active 60 sec <br>

# Web server <br>
Can Hard reset from web server<br>