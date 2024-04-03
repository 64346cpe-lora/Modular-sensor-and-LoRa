from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
import datetime
import serial

import Blynk.BlynkLib as BlynkLib
import RPi.GPIO as GPIO
from Blynk.BlynkTimer import BlynkTimer
import time

BLYNK_AUTH_TOKEN_BOX_SENSOR = "vqDEKRMfj4SEdhQ6mU80EJ_HOAioW9ne"
BLYNK_AUTH_TOKEN_BOX_WATER_PUMP = "oqXzm20LUlEm3p_LG6qsuCT5E9rsn8My"


# Initialize Blynk
box_in = BlynkLib.Blynk(BLYNK_AUTH_TOKEN_BOX_SENSOR)
box_out = BlynkLib.Blynk(BLYNK_AUTH_TOKEN_BOX_WATER_PUMP)

# Create BlynkTimer Instance
timer = BlynkTimer()

@box_in.on("connected")
def blynk_connected():
    print("---------------------boxin---------------------------")
    #batt_in
    box_in.sync_virtual(6)
    box_in.sync_virtual(19)
    box_in.sync_virtual(9)
    #tempinbox
    box_in.sync_virtual(0)
    box_in.sync_virtual(14)
    box_in.sync_virtual(11)
    box_in.sync_virtual(12)
    #tempinair
    box_in.sync_virtual(1)
    box_in.sync_virtual(15)
    box_in.sync_virtual(16)
    box_in.sync_virtual(17)
    #huminbox
    box_in.sync_virtual(2)
    box_in.sync_virtual(24)
    box_in.sync_virtual(20)
    box_in.sync_virtual(21)
    #huminair
    box_in.sync_virtual(3)
    box_in.sync_virtual(28)
    box_in.sync_virtual(26)
    box_in.sync_virtual(27)
    #huminsoil
    box_in.sync_virtual(4)
    box_in.sync_virtual(29) 
    box_in.sync_virtual(31)
    box_in.sync_virtual(32)
    
    box_in.sync_virtual(35)

@box_out.on("connected")
def blynk_connected():
    print("---------------------boxout---------------------------")
    #batt_out
    box_out.sync_virtual(2)
    box_out.sync_virtual(8)
    box_out.sync_virtual(5)
    
    #tempinbox_out
    box_out.sync_virtual(0)
    box_out.sync_virtual(42)
    box_out.sync_virtual(43)
    box_out.sync_virtual(44)

	#huminbox_out
    box_out.sync_virtual(1)
    box_out.sync_virtual(46)
    box_out.sync_virtual(48)
    box_out.sync_virtual(49)

    #switchallday
    box_out.sync_virtual(9)
	
    #rangeone
    box_out.sync_virtual(20)
    box_out.sync_virtual(10)
    box_out.sync_virtual(11)
    box_out.sync_virtual(19)

    #rangetwo
    box_out.sync_virtual(21)
    box_out.sync_virtual(26)
    box_out.sync_virtual(31)
    box_out.sync_virtual(36)
    
    #rangethree
    box_out.sync_virtual(22)
    box_out.sync_virtual(27)
    box_out.sync_virtual(32)
    box_out.sync_virtual(37)
    
    #rangefour
    box_out.sync_virtual(23)
    box_out.sync_virtual(28)
    box_out.sync_virtual(33)
    box_out.sync_virtual(38)
    
    #rangefive
    box_out.sync_virtual(24)
    box_out.sync_virtual(29)
    box_out.sync_virtual(34)
    box_out.sync_virtual(39)

    #rangesix
    box_out.sync_virtual(25)
    box_out.sync_virtual(30)
    box_out.sync_virtual(35)
    box_out.sync_virtual(40)
    
    box_out.sync_virtual(13)
    box_out.sync_virtual(12)
    box_out.sync_virtual(14)
    box_out.sync_virtual(15)
    box_out.sync_virtual(16)
    box_out.sync_virtual(17)
    box_out.sync_virtual(18)
    
    #pump
    box_out.sync_virtual(41)
    
    box_out.sync_virtual(50)
    #Set pump with box_in Humidity
    box_out.sync_virtual(51)
    box_out.sync_virtual(52)
    
@box_in.on("V1")
def blynk_handle_vpins(value):
    settempinair = float(value[0])
    lora.setTempinair(settempinair)
    print("----------------------------------UPDATE--------------------------------------")
    print("settempinair ",settempinair)
    
@box_in.on("V2")
def blynk_handle_vpins(value):
    sethuminbox = float(value[0])
    lora.setHuminbox(sethuminbox)
    print("----------------------------------UPDATE--------------------------------------")
    print("sethuminbox ",sethuminbox)

@box_in.on("V3")
def blynk_handle_vpins(value):
    sethuminair = float(value[0])
    lora.setHuminair(sethuminair)
    print("----------------------------------UPDATE--------------------------------------")
    print("sethuminair ",sethuminair)

@box_in.on("V4")
def blynk_handle_vpins(value):
    sethuminsoil = float(value[0])
    lora.setHuminsoil(sethuminsoil)
    print("----------------------------------UPDATE--------------------------------------")
    print("sethuminsoil ",sethuminsoil)

@box_in.on("V5")
def blynk_handle_vpins(value):
    setlight = float(value[0])
    lora.setLight(setlight)
    print("----------------------------------UPDATE--------------------------------------")
    print("setlight ",setlight)

@box_in.on("V6")
def blynk_handle_vpins(value):
    setbatt_in = float(value[0])
    lora.setBatt_in(setbatt_in)
    print("----------------------------------UPDATE--------------------------------------")
    print("setbatt_in ",setbatt_in)

@box_in.on("V7")
def blynk_handle_vpins(value):
    hardreset_boxin = float(value[0])
    lora.hardResetboxin(hardreset_boxin)
    print("----------------------------------UPDATE--------------------------------------")
    print("hardreset_boxin ",hardreset_boxin)


@box_in.on("V9")
def blynk_handle_vpins(value):
    setalertbatt_in = float(value[0])
    lora.setAlertBatt_in(setalertbatt_in)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalertbatt_in ",setalertbatt_in)


@box_in.on("V11")
def blynk_handle_vpins(value):
    setalerttempboxlow_in = float(value[0])
    lora.setAlertTempBoxLow_in(setalerttempboxlow_in)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalerttempboxlow_in",setalerttempboxlow_in)

@box_in.on("V12")
def blynk_handle_vpins(value):
    setalerttempboxhigh_in = float(value[0])
    lora.setAlertTempBoxHigh_in(setalerttempboxhigh_in)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalerttempboxhigh_in",setalerttempboxhigh_in)

@box_in.on("V14")
def blynk_handle_vpins(value):
    setswitchtempboxin = float(value[0])
    lora.setSwitchtempboxin(setswitchtempboxin)
    print("----------------------------------UPDATE--------------------------------------")
    print("setswitchtempboxin ",setswitchtempboxin)

@box_in.on("V15")
def blynk_handle_vpins(value):
    setswitchtempboxair = float(value[0])
    lora.setSwitchtempboxair(setswitchtempboxair)
    print("----------------------------------UPDATE--------------------------------------")
    print("setswitchtempboxair ",setswitchtempboxair)


@box_in.on("V16")
def blynk_handle_vpins(value):
    setalerttempairlow_in = float(value[0])
    lora.setAlertTempAirLow_in(setalerttempairlow_in)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalerttempairlow_in",setalerttempairlow_in)

@box_in.on("V17")
def blynk_handle_vpins(value):
    setalerttempairhigh_in = float(value[0])
    lora.setAlertTemAirHigh_in(setalerttempairhigh_in)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalerttempairhigh_in",setalerttempairhigh_in)

@box_in.on("V19")
def blynk_handle_vpins(value):
    setswitcbattin = float(value[0])
    lora.setSwitcbattin(setswitcbattin)
    print("----------------------------------UPDATE--------------------------------------")
    print("setswitcbattin ",setswitcbattin)
    

@box_in.on("V20")
def blynk_handle_vpins(value):
    setalerthumboxlow_in = float(value[0])
    lora.setAlertHumBoxLow_in(setalerthumboxlow_in)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalerthumboxlow_in",setalerthumboxlow_in)    

@box_in.on("V21")
def blynk_handle_vpins(value):
    setalerthumboxhigh_in = float(value[0])
    lora.setAlertHumBoxHigh_in(setalerthumboxhigh_in)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalerthumboxhigh_in",setalerthumboxhigh_in)   
    
@box_in.on("V24")
def blynk_handle_vpins(value):
    setswitchhumboxin = float(value[0])
    lora.setSwitchHumboxin(setswitchhumboxin)
    print("----------------------------------UPDATE--------------------------------------")
    print("setswitchhumboxin ",setswitchhumboxin)



@box_in.on("V26")
def blynk_handle_vpins(value):
    setalerthumairlow_in = float(value[0])
    lora.setAlertHumAirLow_in(setalerthumairlow_in)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalerthumairlow_in",setalerthumairlow_in)    
    
@box_in.on("V27")
def blynk_handle_vpins(value):
    setalerthumairhigh_in = float(value[0])
    lora.setAlertHumAirHigh_in(setalerthumairhigh_in)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalerthumairhigh_in",setalerthumairhigh_in)  
     
@box_in.on("V28")
def blynk_handle_vpins(value):
    setswitchhumairin = float(value[0])
    lora.setSwitchHumairin(setswitchhumairin)
    print("----------------------------------UPDATE--------------------------------------")
    print("setswitchhumairin ",setswitchhumairin)


@box_in.on("V29")
def blynk_handle_vpins(value):
    setswitchhumsoilin = float(value[0])
    lora.setSwitchHumsoilin(setswitchhumsoilin)
    print("----------------------------------UPDATE--------------------------------------")
    print("setswitchhumsoilin ",setswitchhumsoilin)

@box_in.on("V31")
def blynk_handle_vpins(value):
    setalerthumsoillow_in = float(value[0])
    lora.setAlertHumSoilLow_in(setalerthumsoillow_in)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalerthumsoillow_in",setalerthumsoillow_in)    

@box_in.on("V32")
def blynk_handle_vpins(value):
    setalerthumsoilhigh_in = float(value[0])
    lora.setAlertHumSoilHigh_in(setalerthumsoilhigh_in)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalerthumsoilhigh_in",setalerthumsoilhigh_in)  
    
 ####################################################   
@box_out.on("V0")
def blynk_handle_vpins(value):
    settempoutbox_out = float(value[0])
    lora.setBatt_out(settempoutbox_out)
    print("----------------------------------UPDATE--------------------------------------")
    print("setbatt_out ",settempoutbox_out)    
    
@box_out.on("V42")
def blynk_handle_vpins(value):
    setswitchtempinbox_out = float(value[0])
    lora.setSwitchtempboxout(setswitchtempinbox_out)
    print("----------------------------------UPDATE--------------------------------------")
    print("setswitchtempinbox_out ",setswitchtempinbox_out)

@box_out.on("V43")
def blynk_handle_vpins(value):
    setalerttempinboxlow_out = float(value[0])
    lora.setAlertTempBoxLow_out(setalerttempinboxlow_out)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalerttempinboxlow_out ",setalerttempinboxlow_out)


@box_out.on("V44")
def blynk_handle_vpins(value):
    setalerttempinboxhigh_out = float(value[0])
    lora.setAlertTempBoxHigh_out(setalerttempinboxhigh_out)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalerttempinboxhigh_out ",setalerttempinboxhigh_out)



@box_out.on("V1")
def blynk_handle_vpins(value):
    sethumoutbox = float(value[0])
    lora.setHumoutbox(sethumoutbox)
    print("----------------------------------UPDATE--------------------------------------")
    print("sethumoutbox ",sethumoutbox)

@box_out.on("V46")
def blynk_handle_vpins(value):
    setswitchhumboxout = float(value[0])
    lora.setSwitchHumboxout(setswitchhumboxout)
    print("----------------------------------UPDATE--------------------------------------")
    print("setswitchhumboxout ",setswitchhumboxout)

@box_out.on("V48")
def blynk_handle_vpins(value):
    setalerthumboxlow_out = float(value[0])
    lora.setAlertHumBoxLow_out(setalerthumboxlow_out)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalerthumboxlow_out ",setalerthumboxlow_out)

@box_out.on("V49")
def blynk_handle_vpins(value):
    setalerthumboxhigh_out = float(value[0])
    lora.setAlertHumBoxHigh_out(setalerthumboxhigh_out)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalerthumboxhigh_out ",setalerthumboxhigh_out)

@box_out.on("V2")
def blynk_handle_vpins(value):
    setbatt_out = float(value[0])
    lora.setBatt_out(setbatt_out)
    print("----------------------------------UPDATE--------------------------------------")
    print("setbatt_out ",setbatt_out)

@box_out.on("V5")
def blynk_handle_vpins(value):
    setalertbatt_out = float(value[0])
    lora.setAlertBatt_out(setalertbatt_out)
    print("----------------------------------UPDATE--------------------------------------")
    print("setalertbatt_boxout ",setalertbatt_out)
    
@box_out.on("V8")
def blynk_handle_vpins(value):
    setswitcbattout = float(value[0])
    lora.setSwitcbattout(setswitcbattout)
    print("----------------------------------UPDATE--------------------------------------")
    print("setswitcbattout ",setswitcbattout)

@box_out.on("V7")
def blynk_handle_vpins(value):
	hardreset_boxout = float(value[0])
	if(hardreset_boxout == 1):
	#lora.hardResetboxout(hardreset_boxout)
		lora.hardResetboxout(hardreset_boxout)
	print("----------------------------------UPDATE--------------------------------------")
	print("hardreset_boxout ",hardreset_boxout)


@box_out.on("V9")
def blynk_handle_vpins(value):
    allday = float(value[0])
    lora.setAllday(allday)
    print("----------------------------------UPDATE--------------------------------------")
    print("allday ",allday)


    
@box_out.on("V12")
def blynk_handle_vpins(value):
    setstatusmonday = float(value[0])
    lora.setstatusMonday(setstatusmonday)
    print("----------------------------------UPDATE--------------------------------------")
    print("setstatusMonday ",setstatusmonday)
    
@box_out.on("V13")
def blynk_handle_vpins(value):
    setstatussunday = float(value[0])
    lora.setstatusSunday(setstatussunday)
    print("----------------------------------UPDATE--------------------------------------")
    print("setstatusSunday ",setstatussunday)
    
@box_out.on("V14")
def blynk_handle_vpins(value):
    setstatustuesday = float(value[0])
    lora.setstatusTuesday(setstatustuesday)
    print("----------------------------------UPDATE--------------------------------------")
    print("setstatusTuesday ",setstatustuesday)
    
@box_out.on("V15")
def blynk_handle_vpins(value):
    setstatuswednesday = float(value[0])
    lora.setstatusWednesday(setstatuswednesday)
    print("----------------------------------UPDATE--------------------------------------")
    print("setstatusWednesday ",setstatuswednesday)
    
@box_out.on("V16")
def blynk_handle_vpins(value):
    setstatusthursday = float(value[0])
    lora.setstatusThursday(setstatusthursday)
    print("----------------------------------UPDATE--------------------------------------")
    print("setstatusThursday ",setstatusthursday)
    
@box_out.on("V17")
def blynk_handle_vpins(value):
    setstatusfriday = float(value[0])
    lora.setstatusFriday(setstatusfriday)
    print("----------------------------------UPDATE--------------------------------------")
    print("setstatusFriday ",setstatusfriday)
    
@box_out.on("V18")
def blynk_handle_vpins(value):
    setstatussaturday = float(value[0])
    lora.setstatusSaturday(setstatussaturday)
    print("----------------------------------UPDATE--------------------------------------")
    print("setstatusSaturday ",setstatussaturday)

#############################333
    
#rangeone

@box_out.on("V20")
def blynk_handle_vpins(value):
    setswitchrangeone = float(value[0])
    lora.setSwitchRangeOne(setswitchrangeone)
    print("----------------------------------UPDATE--------------------------------------")
    print("setwaitpumpone ",setswitchrangeone)

@box_out.on("V10")
def blynk_handle_vpins(value):
    sethourone = int(value[0])
    lora.setHourOne(sethourone)
    print("----------------------------------UPDATE--------------------------------------")
    print("sethourone ",sethourone)

@box_out.on("V11")
def blynk_handle_vpins(value):
    setminuteone = int(value[0])
    lora.setMinuteOne(setminuteone)
    print("----------------------------------UPDATE--------------------------------------")
    print("setminuteone ",setminuteone)
    
@box_out.on("V19")
def blynk_handle_vpins(value):
    setwaitpumpone = float(value[0])
    lora.setWaitpumpOne(setwaitpumpone)
    print("----------------------------------UPDATE--------------------------------------")
    print("setwaitpumpone ",setwaitpumpone)

#rangetwo

@box_out.on("V21")
def blynk_handle_vpins(value):
    setswitchrangetwo = float(value[0])
    lora.setSwitchRangeTwo(setswitchrangetwo)
    print("----------------------------------UPDATE--------------------------------------")
    print("setswitchrangetwo ",setswitchrangetwo)


@box_out.on("V26")
def blynk_handle_vpins(value):
    sethourtwo = int(value[0])
    lora.setHourTwo(sethourtwo)
    print("----------------------------------UPDATE--------------------------------------")
    print("sethourtwo ",sethourtwo)

@box_out.on("V31")
def blynk_handle_vpins(value):
    setminutetwo = int(value[0])
    lora.setMinuteTwo(setminutetwo)
    print("----------------------------------UPDATE--------------------------------------")
    print("setminutetwo ",setminutetwo)
    
@box_out.on("V36")
def blynk_handle_vpins(value):
    setwaitpumptwo = float(value[0])
    lora.setWaitpumpTwo(setwaitpumptwo)
    print("----------------------------------UPDATE--------------------------------------")
    print("setwaitpumptwo ",setwaitpumptwo)

#rangethree

@box_out.on("V22")
def blynk_handle_vpins(value):
    setswitchrangethree = float(value[0])
    lora.setSwitchRangeThree(setswitchrangethree)
    print("----------------------------------UPDATE--------------------------------------")
    print("setswitchrangethree ",setswitchrangethree)


@box_out.on("V27")
def blynk_handle_vpins(value):
    sethourthree = int(value[0])
    lora.setHourThree(sethourthree)
    print("----------------------------------UPDATE--------------------------------------")
    print("sethourthree ",sethourthree)

@box_out.on("V32")
def blynk_handle_vpins(value):
    setminutethree = int(value[0])
    lora.setMinuteThree(setminutethree)
    print("----------------------------------UPDATE--------------------------------------")
    print("setminutethree ",setminutethree)
    
@box_out.on("V37")
def blynk_handle_vpins(value):
    setwaitpumpthree = float(value[0])
    lora.setWaitpumpThree(setwaitpumpthree)
    print("----------------------------------UPDATE--------------------------------------")
    print("setwaitpumpthree ",setwaitpumpthree)    

#rangefour

@box_out.on("V23")
def blynk_handle_vpins(value):
    setswitchrangefour = float(value[0])
    lora.setSwitchRangeFour(setswitchrangefour)
    print("----------------------------------UPDATE--------------------------------------")
    print("setswitchrangefour ",setswitchrangefour)


@box_out.on("V28")
def blynk_handle_vpins(value):
    sethourfour = int(value[0])
    lora.setHourFour(sethourfour)
    print("----------------------------------UPDATE--------------------------------------")
    print("sethourfour ",sethourfour)

@box_out.on("V33")
def blynk_handle_vpins(value):
    setminutetfour = int(value[0])
    lora.setMinuteFour(setminutetfour)
    print("----------------------------------UPDATE--------------------------------------")
    print("setminutetfour ",setminutetfour)
    
@box_out.on("V38")
def blynk_handle_vpins(value):
    setwaitpumpfour = float(value[0])
    lora.setWaitpumpFour(setwaitpumpfour)
    print("----------------------------------UPDATE--------------------------------------")
    print("setwaitpumpfour ",setwaitpumpfour)    


#rangefive

@box_out.on("V24")
def blynk_handle_vpins(value):
    setswitchrangefive = float(value[0])
    lora.setSwitchRangeFive(setswitchrangefive)
    print("----------------------------------UPDATE--------------------------------------")
    print("setswitchrangefive ",setswitchrangefive)


@box_out.on("V29")
def blynk_handle_vpins(value):
    sethourfive = int(value[0])
    lora.setHourFive(sethourfive)
    print("----------------------------------UPDATE--------------------------------------")
    print("sethourfive ",sethourfive)

@box_out.on("V34")
def blynk_handle_vpins(value):
    setminutetfive = int(value[0])
    lora.setMinuteFive(setminutetfive)
    print("----------------------------------UPDATE--------------------------------------")
    print("setminutetfive ",setminutetfive)
    
@box_out.on("V39")
def blynk_handle_vpins(value):
    setwaitpumpfive = float(value[0])
    lora.setWaitpumpFive(setwaitpumpfive)
    print("----------------------------------UPDATE--------------------------------------")
    print("setwaitpumpfive ",setwaitpumpfive)    


#rangesix

@box_out.on("V25")
def blynk_handle_vpins(value):
    setswitchrangesix = float(value[0])
    lora.setSwitchRangeSix(setswitchrangesix)
    print("----------------------------------UPDATE--------------------------------------")
    print("setswitchrangesix ",setswitchrangesix)


@box_out.on("V30")
def blynk_handle_vpins(value):
    sethoursix = int(value[0])
    lora.setHourSix(sethoursix)
    print("----------------------------------UPDATE--------------------------------------")
    print("sethoursix ",sethoursix)

@box_out.on("V35")
def blynk_handle_vpins(value):
    setminutetsix = int(value[0])
    lora.setMinuteSix(setminutetsix)
    print("----------------------------------UPDATE--------------------------------------")
    print("setminutetsix ",setminutetsix)
    
@box_out.on("V40")
def blynk_handle_vpins(value):
    setwaitpumpsix = float(value[0])
    lora.setWaitpumpSix(setwaitpumpsix)
    print("----------------------------------UPDATE--------------------------------------")
    print("setwaitpumpsix ",setwaitpumpsix)    


#set pump active on blynk
@box_out.on("V41")
def blynk_handle_vpins(value):
	statusPump = int(value[0])
	lora.setStatusPump(statusPump)
	print("----------------------------------UPDATE--------------------------------------")
	print("status pump ",statusPump)
	lora.statusBox = True
	lora.statusBoxout = True
	lora.send_data_to_box_out(True)
	print("status pump ",statusPump)

@box_out.on("V50")
def blynk_handle_vpins(value):
	status_led_pump = int(value[0])
	print("----------------------------------UPDATE--------------------------------------")
	print("status led pump ",status_led_pump)
@box_out.on("V51")
def blynk_handle_vpins(value):
	status_pump_working_by_humidity = int(value[0])
	lora.setStatusPumpWorkingByHumidity(status_pump_working_by_humidity)
	print("----------------------------------UPDATE--------------------------------------")
	print("status pump working by humidity ",status_pump_working_by_humidity)

@box_out.on("V52")
def blynk_handle_vpins(value):
	humidity_pump_working = int(value[0])
	lora.setHumidityPumpWorking(humidity_pump_working)
	print("----------------------------------UPDATE--------------------------------------")
	print("humidity pump working ",humidity_pump_working)
	


BOARD.setup()

class LoRaGateway(LoRa):
	def __init__(self, verbose=False):
		super(LoRaGateway, self).__init__(verbose)
		self.set_mode(MODE.SLEEP)
		self.set_dio_mapping([0] * 6)
		self.address_gateway ="255"
		self.address_in = "170"
		self.address_out = "186"
		self.setalertbatt_in = 0
		self.setalertbatt_out = 0
		self.battery_boxin=0
		self.battery_boxout=0
		self.receivedboxout_data = 0
		self.receivedboxin_data = 0
		self.tempinbox_in = 0
		self.tempinair = 0
		self.humi_soil = 0
		self.last_humi_soil = 0
		self.statePump = 0
		self.statusPump = 0
		self.pumpWorkByHumiDone = False
		self.statusPumpOnBoxOut = 0
		
		self.statusBox = False
		self.statusBoxin = False
		self.statusBoxout = False
		self.statusBoxinblynk = False
		self.statusBoxoutblynk = False
		self.statusBoxinfail=False
		self.statusBoxoutfail=False
		
		self.time_alert_receive_in = datetime.datetime.now() + datetime.timedelta(minutes=10)
		self.time_alert_receive_out = datetime.datetime.now() + datetime.timedelta(minutes=10)
		self.current_time = datetime.datetime.now()
		
		self.temp0 = 0
		self.aleartbatt = 0;
		self.hardresetboxin = 0
		self.hardresetboxout = 0
		self.next_time = datetime.datetime.now() + datetime.timedelta(seconds=1)
		self.next_time1 = datetime.datetime.now() + datetime.timedelta(seconds=1)
		self.setalerttempboxhigh_in = 0
		self.setalerttempboxlow_in = 0
		self.setalerttempairlow_in = 0
		self.setalerttempairhigh_in = 0
        
		self.setalerthumairlow_in=0
		self.setalerthumairhigh_in=0
		self.setswitchhumairin=0
        
		self.setswitchhumsoilin=0
		self.setalerthumsoillow_in=0
		self.setalerthumsoilhigh_in=0
        
		self.sethourone=0
		self.setminute=0
		self.setwaitpump=0
		self.setwaitpumpone=0
		self.setmonday=""
		self.setsunday=""
		self.settuesday = ""
		self.setwednesday = ""
		self.setthursday = ""
		self.setfriday = ""
		self.setsaturday = ""
        
		self.datelocal=""
		self.hourandmin=''
		self.activepump = 0
		self.setswitchtempboxin = 0
		self.setswitchtempboxair = 0
		self.setswitchtempairin = 0
		self.setswitcbattin =0
		self.setswitcbattout =0
		self.setalerthumboxlow_in =0
		self.setalerthumboxhigh_in=0
		self.huminbox = 0
		self.setswitchhumboxin=0	
		self.setalerthumboxlow_out = 0
		self.setalerthumboxhigh_out = 0
		self.setswitchhumboxout =0   
        
		self.tempoutbox_out = 0
		self.setalerttempboxlow_out=0
		self.setalerttempboxhigh_out=0
		
		self.statusPump = 0
		self.statusPumpOnWeb = 4
		self.statusPumpOnBoxOut = 0;
		self.pumpHumidity = 0
		self.humidityPumpStart = 0
		box_out.virtual_write(41,4)
		
		
		
	def setStatusPumpWorkingByHumidity(self, status):
		self.pumpHumidity = status
		
	def setHumidityPumpWorking(self, humidity):
		self.humidityPumpStart = humidity
		
	def setAllday(self, setallday):
		self.setallday = setallday
		if(self.setallday==1):
			box_out.virtual_write(12, 1)  
			box_out.virtual_write(13, 1)
			box_out.virtual_write(14, 1)
			box_out.virtual_write(15, 1)
			box_out.virtual_write(16, 1)
			box_out.virtual_write(17, 1)
			box_out.virtual_write(18, 1)
		else:
			box_out.virtual_write(12, 0)  
			box_out.virtual_write(13, 0)
			box_out.virtual_write(14, 0)
			box_out.virtual_write(15, 0)
			box_out.virtual_write(16, 0)
			box_out.virtual_write(17, 0)
			box_out.virtual_write(18, 0)
        
		box_out.sync_virtual(12)
		box_out.sync_virtual(13)
		box_out.sync_virtual(14)
		box_out.sync_virtual(15)
		box_out.sync_virtual(16)
		box_out.sync_virtual(17)
		box_out.sync_virtual(18)
    
    
        
    
	def setstatusMonday(self, setstatusmonday):
		self.setstatusmonday = setstatusmonday
		if(self.setstatusmonday==1):
			self.setmonday = "Monday"
		else:
			self.setmonday = ""
            
	def setstatusSunday(self, setstatussunday):
		self.setstatussunday = setstatussunday
		if(self.setstatussunday==1):
			self.setsunday = "Sunday"
		else:
			self.setsunday = ""
            
	def setstatusTuesday(self, setstatustuesday):
		self.setstatustuesday = setstatustuesday
		if(self.setstatustuesday==1):
			self.settuesday = "Tuesday"
		else:
			self.settuesday = ""            

	def setstatusWednesday(self, setstatuswednesday):
		self.setstatuswednesday = setstatuswednesday
		if(self.setstatuswednesday==1):
			self.setwednesday = "Wednesday"
		else:
			self.setwednesday = ""
	def setstatusThursday(self, setstatusthursday):
		self.setstatusthursday = setstatusthursday
		if(self.setstatusthursday==1):
			self.setthursday = "Thursday"
		else:
			self.setthursday = ""
            
	def setstatusFriday(self, setstatusfriday):
		self.setstatusfriday = setstatusfriday
		if(self.setstatusfriday==1):
			self.setfriday = "Friday"
		else:
			self.setfriday = ""
	def setstatusSaturday(self, setstatussaturday):
		self.setstatussaturday = setstatussaturday
		if(self.setstatussaturday==1):
			self.setsaturday = "Saturday"
		else:
			self.setsaturday = ""   
    
    #battin
	def setBatt_in(self, setbatt_in):
		self.battery_boxin = setbatt_in
    
	def setSwitcbattin(self, setswitcbattin):
		self.setswitcbattin = setswitcbattin
		self.checkAlertBatt_in()
    
	def setAlertBatt_in(self, setalertbatt_in):
		self.setalertbatt_in = setalertbatt_in
		self.checkAlertBatt_in()
    
	def checkAlertBatt_in(self):
		if self.setswitcbattin == 1:
			print("การแจ้งเตือนแบต",self.battery_boxin,"<",self.setalertbatt_in)
			if(self.battery_boxin<self.setalertbatt_in): #50<51
				box_in.virtual_write(8, 1)
				box_in.log_event("batt_alarm", "แบตเตอรี่ต่ำกว่าค่าที่กำหนด")
			else:
				box_in.virtual_write(8, 0)
		else:
			box_in.virtual_write(8, 0)
    
    #tempinbox
	def setTempinbox(self, settempinbox):
		self.tempinbox_in = settempinbox
		self.checkAleartTempBox_in()
    
	def setSwitchtempboxin(self, setswitchtempboxin):
		self.setswitchtempboxin = setswitchtempboxin
		self.checkAleartTempBox_in()
        
	def setAlertTempBoxLow_in(self, setalerttempboxlow_in):
		self.setalerttempboxlow_in = setalerttempboxlow_in
		self.checkAleartTempBox_in()
    
	def setAlertTempBoxHigh_in(self, setalerttempboxhigh_in):
		self.setalerttempboxhigh_in = setalerttempboxhigh_in
		self.checkAleartTempBox_in()
    
	def checkAleartTempBox_in(self):
       # print(self.tempinbox_in,"<",self.setalerttempboxlow_in," or ", self.tempinbox_in ">",self.setalerttempboxhigh_in )
		if self.setswitchtempboxin == 1:
			if self.tempinbox_in < self.setalerttempboxlow_in: # temp < setlow or 
				box_in.virtual_write(10, 1)
				box_in.log_event("temp_box_alarm", "อุณหภูมิในกล่องต่ำกว่าที่กำหนด")
			elif self.tempinbox_in > self.setalerttempboxhigh_in : #temp > sethigh
				box_in.virtual_write(10, 0)
				box_in.log_event("temp_box_alarm", "อุณหภูมิในกล่องสูงกว่าที่กำหนด")
			else :
				box_in.virtual_write(10, 0)
		else:
			box_in.virtual_write(10, 0)
    
                
    
    #tempinair
	def setTempinair(self, settempinair):
		self.tempinair = settempinair
		self.checkAleartTempAir_in()
        
	def setSwitchtempboxair(self, setswitchtempboxair):
		self.setswitchtempboxair = setswitchtempboxair
		self.checkAleartTempAir_in()
    
	def setAlertTempAirLow_in(self, setalerttempairlow_in):
			self.setalerttempairlow_in = setalerttempairlow_in
			self.checkAleartTempAir_in()    
    
	def setAlertTemAirHigh_in(self, setalerttempairhigh_in):
			self.setalerttempairhigh_in = setalerttempairhigh_in
			self.checkAleartTempAir_in()
    
    
	def checkAleartTempAir_in(self):
		if self.setswitchtempboxair == 1:
			print(self.tempinair,"<",self.setalerttempairlow_in," or ",self.tempinair,">",self.setalerttempairhigh_in)
			if self.tempinair < self.setalerttempairlow_in : # temp < setlow
				box_in.virtual_write(18, 1)
				box_in.log_event("temp_air_alarm", "อุณหภูมิในกล่องต่ำกว่าที่กำหนด")
			elif self.tempinair > self.setalerttempairhigh_in :
				box_in.virtual_write(18, 1)
				box_in.log_event("temp_air_alarm", "อุณหภูมิในกล่องสูงกว่าที่กำหนด") # temp > sethigh
			else:
				box_in.virtual_write(18, 0)
		else:
			box_in.virtual_write(18, 0)
    
    #huminbox
	def setHuminbox(self, sethuminbox):
		self.huminbox = sethuminbox
		self.checkAlartHumBox_in()
        
	def setSwitchHumboxin(self, setswitchhumboxin):
		self.setswitchhumboxin = setswitchhumboxin
		self.checkAlartHumBox_in()
    
	def setAlertHumBoxLow_in(self, setalerthumboxlow_in):
		self.setalerthumboxlow_in = setalerthumboxlow_in
		self.checkAlartHumBox_in()
    
	def setAlertHumBoxHigh_in(self, setalerthumboxhigh_in):
		self.setalerthumboxhigh_in = setalerthumboxhigh_in
		self.checkAlartHumBox_in()
    
	def checkAlartHumBox_in(self):
		print (self.huminbox ,"<",self.setalerthumboxlow_in," or ",self.huminbox,">",self.setalerthumboxhigh_in)
		if self.setswitchhumboxin == 1:
			if self.huminbox < self.setalerthumboxlow_in :
				box_in.virtual_write(22, 1)
				box_in.log_event("humi_box_alarm", "ความชื้นในกล่องต่ำกว่าที่กำหนด")
			elif self.huminbox > self.setalerthumboxhigh_in:
				box_in.virtual_write(22, 1)
				box_in.log_event("humi_box_alarm", "ความชื้นในกล่องสูงกว่าที่กำหนด")
			else:
				box_in.virtual_write(22, 0)
		else:
			box_in.virtual_write(22, 0)
    
    
    
    #huminair
	def setHuminair(self, sethuminair):
		self.huminair = sethuminair
		self.checkAlartHumAir_in()   
   
	def setSwitchHumairin(self, setswitchhumairin):
		self.setswitchhumairin = setswitchhumairin
		self.checkAlartHumAir_in()
     
	def setAlertHumAirLow_in(self, setalerthumairlow_in):
		self.setalerthumairlow_in = setalerthumairlow_in
		self.checkAlartHumAir_in()
    
	def setAlertHumAirHigh_in(self, setalerthumairhigh_in):
		self.setalerthumairhigh_in = setalerthumairhigh_in
		self.checkAlartHumAir_in()
        
	def checkAlartHumAir_in(self):
		print (self.huminair ,"<",self.setalerthumairlow_in," or ",self.huminair,">",self.setalerthumairhigh_in)
		if self.setswitchhumairin == 1:
			if self.huminair < self.setalerthumairlow_in :
				box_in.virtual_write(25, 1)
				box_in.log_event("humi_air_alarm", "ความชื้นในอากาศต่ำกว่าที่กำหนด")
			elif self.huminair > self.setalerthumairhigh_in :
				box_in.virtual_write(25, 1)
				box_in.log_event("temp_air_alarm", "ความชื้นในอากาศสูงกว่าที่กำหนด")
			else:
				box_in.virtual_write(25, 0)
		else:
			box_in.virtual_write(25, 0)
    
    #huminsoil
	def setHuminsoil(self, sethuminsoil):
		self.huminsoil = sethuminsoil
		self.checkAlartHumSoil_in()   
	
	def setSwitchHumsoilin(self, setswitchhumsoilin):
		self.setswitchhumsoilin = setswitchhumsoilin
		self.checkAlartHumSoil_in()
        
	def setAlertHumSoilLow_in(self, setalerthumsoillow_in):
		self.setalerthumsoillow_in = setalerthumsoillow_in
		self.checkAlartHumSoil_in()
    
    
	def setAlertHumSoilHigh_in(self, setalerthumsoilhigh_in):
		self.setalerthumsoilhigh_in = setalerthumsoilhigh_in
		self.checkAlartHumSoil_in()
        
	def checkAlartHumSoil_in(self):
		print (self.huminsoil ,"<",self.setalerthumsoillow_in," or ",self.huminsoil,">",self.setalerthumsoilhigh_in)
		if self.setswitchhumsoilin == 1:
			if self.huminsoil < self.setalerthumsoillow_in :
				box_in.virtual_write(30, 1)
				box_in.log_event("humi_soil_alarm", "ความชื้นในดินต่ำกว่าที่กำหนด")
			elif self.huminsoil > self.setalerthumsoilhigh_in :
				box_in.virtual_write(30, 1)
				box_in.log_event("humi_soil_alarm", "ความชื้นในดินสูงกว่าที่กำหนด")
			else:
				box_in.virtual_write(30, 0)
		else:
			box_in.virtual_write(30, 0)
        
        
    #light
	def setLight(self, setlight):
		self.light = sethuminsoil
    
    #hardReset_boxin
	def hardResetboxin(self, hardreset_boxin):
		self.hardresetboxin = 1    
    
    #battout
	def setBatt_out(self, setbatt_out):
		self.battery_boxout = setbatt_out
        
	def setSwitcbattout(self, setswitcbattout):
		self.setswitcbattout = setswitcbattout
		self.checkAlertBatt_out()
        
        
	def setAlertBatt_out(self, setalertbatt_out):
			self.setalertbatt_out = setalertbatt_out
			self.checkAlertBatt_out()
    
	def checkAlertBatt_out(self):
		if self.setswitcbattout ==1:
			if(self.battery_boxout<self.setalertbatt_out): #
				box_out.virtual_write(6, 1)
				print("Alert Batttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
				box_out.log_event("batt_alarm", "แบตเตอรีต่ำกว่าค่าที่กำหนด")
			else:
				box_out.virtual_write(6, 0)
		else:
			box_out.virtual_write(6, 0)
            
    
                
    #hardReset_boxout
	def hardResetboxout(self, hardreset_boxout):
		self.hardresetboxout = 1
    
    
    #tempinbox_out
	def setTempoutbox(self, settempoutbox):
		self.tempinbox_out = settempoutbox
		self.checkAleartTempBox_out()
    
	def setSwitchtempboxout(self, setswitchtempboxout):
		self.setswitchtempboxout = setswitchtempboxout
		self.checkAleartTempBox_out()
        
	def setAlertTempBoxLow_out(self, setalerttempboxlow_out):
		self.setalerttempboxlow_out = setalerttempboxlow_out
		self.checkAleartTempBox_out()
    
	def setAlertTempBoxHigh_out(self, setalerttempboxhigh_out):
		self.setalerttempboxhigh_out = setalerttempboxhigh_out
		self.checkAleartTempBox_out()
    
	def checkAleartTempBox_out(self):
		print(self.tempoutbox_out,"<",self.setalerttempboxlow_out," or ", self.tempoutbox_out ,">",self.setalerttempboxhigh_out )
		if self.setswitchtempboxout == 1:
			if self.tempoutbox_out < self.setalerttempboxlow_out: # temp < setlow
				box_out.virtual_write(45, 1)
				box_out.log_event("temp_alarm","อุณหภูมิในกล่องต่ำกว่าที่กำหนด")
			elif self.tempoutbox_out > self.setalerttempboxhigh_out: #temp > sethigh
				box_out.virtual_write(45, 1)
				box_out.log_event("temp_alarm","อุณหภูมิในกล่องสูงกว่าที่กำหนด")
			else:
				box_out.virtual_write(45, 0)
		else:
			box_out.virtual_write(45, 0)
    
     #huminbox_out
	def setHumoutbox(self, sethumoutbox):
		self.humoutbox = sethumoutbox
		self.checkAlartHumBox_out()
        
	def setSwitchHumboxout(self, setswitchhumboxout):
		self.setswitchhumboxout = setswitchhumboxout
		self.checkAlartHumBox_out()
    
	def setAlertHumBoxLow_out(self, setalerthumboxlow_out):
		self.setalerthumboxlow_out = setalerthumboxlow_out
		self.checkAlartHumBox_out()
    
	def setAlertHumBoxHigh_out(self, setalerthumboxhigh_out):
		self.setalerthumboxhigh_out = setalerthumboxhigh_out
		self.checkAlartHumBox_out()
    
	def checkAlartHumBox_out(self):
		print (self.humoutbox ,"<",self.setalerthumboxlow_out," or ",self.humoutbox,">",self.setalerthumboxhigh_out)
		if self.setswitchhumboxout == 1:
			if self.humoutbox < self.setalerthumboxlow_out :
				box_out.virtual_write(47, 1)
				box_out.log_event("humi_alarm","ความชื้นในกล่องต่ำกว่าที่กำหนด")
			elif self.humoutbox > self.setalerthumboxhigh_out:
				box_out.virtual_write(47, 1)
				box_out.log_event("humi_alarm","ความชื้นในกล่องสูงกว่าที่กำหนด")
			else:
				box_out.virtual_write(47, 0)
		else:
			box_out.virtual_write(47, 0)
    
    
    #rangeone
	def setHourOne(self, sethourone):
		self.sethourone = sethourone
    
	def setMinuteOne(self, setminuteone):
		self.setminuteone = setminuteone
    
	def setSwitchRangeOne(self,setswitchrangeone):
		self.setswitchrangeone =setswitchrangeone
        
	def setWaitpumpOne(self, setwaitpumpone):
		self.setwaitpumpone = setwaitpumpone    
    
   #rangetwo
	def setHourTwo(self, sethourtwo):
		self.sethourtwo = sethourtwo
    
	def setMinuteTwo(self, setminutetwo):
		self.setminutetwo = setminutetwo
    
	def setSwitchRangeTwo(self,setswitchrangetwo):
		self.setswitchrangetwo =setswitchrangetwo
        
	def setWaitpumpTwo(self, setwaitpumptwo):
		self.setwaitpumptwo = setwaitpumptwo     
    
	#rangethree
	def setHourThree(self, sethourthree):
		self.sethourthree = sethourthree
    
	def setMinuteThree(self, setminutethree):
		self.setminutethree = setminutethree
    
	def setSwitchRangeThree(self,setswitchrangethree):
		self.setswitchrangethree =setswitchrangethree
        
	def setWaitpumpThree(self, setwaitpumpthree):
		self.setwaitpumpthree = setwaitpumpthree     
    
            
    #rangefour
	def setHourFour(self, sethourfour):
		self.sethourfour = sethourfour
    
	def setMinuteFour(self, setminutefour):
		self.setminutefour = setminutefour
    
	def setSwitchRangeFour(self,setswitchrangefour):
		self.setswitchrangefour =setswitchrangefour
        
	def setWaitpumpFour(self, setwaitpumpfour):
		self.setwaitpumpfour = setwaitpumpfour     
    
    
    #rangefive
	def setHourFive(self, sethourfive):
		self.sethourfive = sethourfive
    
	def setMinuteFive(self, setminutefive):
		self.setminutefive = setminutefive
    
	def setSwitchRangeFive(self,setswitchrangefive):
		self.setswitchrangefive =setswitchrangefive
        
	def setWaitpumpFive(self, setwaitpumpfive):
		self.setwaitpumpfive = setwaitpumpfive 
    
    #rangesix
	def setHourSix(self, sethoursix):
		self.sethoursix = sethoursix
    
	def setMinuteSix(self, setminutesix):
		self.setminutesix = setminutesix
    
	def setSwitchRangeSix(self,setswitchrangesix):
		self.setswitchrangesix =setswitchrangesix
        
	def setWaitpumpSix(self, setwaitpumpsix):
		self.setwaitpumpsix = setwaitpumpsix 
    
	def setStatusPump(self, setStatusPump):
		self.statusPump = setStatusPump
		print("status pump : ", self.statusPump)
    
	def setupMode(self):
			rssi_value = self.get_rssi_value()
			status = self.get_modem_status()
			sys.stdout.flush()
			box_in.run()
			box_out.run()
    
	def updateBlynk(self):
		if self.statusBoxinblynk == True:
			box_in.virtual_write(0, self.tempinbox_in)
			box_in.virtual_write(1, self.tempinair)
			box_in.virtual_write(2, self.huminbox)
			box_in.virtual_write(3, self.huminair)
			box_in.virtual_write(4, self.huminsoil)
			box_in.virtual_write(5, self.light)
			box_in.virtual_write(6, self.battery_boxin)
			box_in.virtual_write(35, 1)
			box_in.virtual_write(36, 0)
			self.checkAleartTempBox_in()
			self.checkAleartTempAir_in()
			self.checkAlertBatt_in()
			self.checkAlartHumBox_in()
			self.checkAlartHumAir_in()
			self.checkAlartHumSoil_in()
			print("upload Boxin to Blynk")
			self.statusBoxinblynk = False
		elif self.statusBoxoutblynk == True:
			box_out.virtual_write(0, self.tempoutbox_out)
			box_out.virtual_write(1, self.humoutbox)
			box_out.virtual_write(2, self.battery_boxout)
			if self.ph != 999 :
				box_out.virtual_write(3, self.ph)
			if self.ec != 999 :
				box_out.virtual_write(4, self.ec)
			box_out.virtual_write(41, self.statusPumpOnBoxOut)	  
			box_out.virtual_write(50, self.statusPumpWorking)
			if self.statusPumpOnBoxOut == 4 :
				box_out.virtual_write(50, 0)
			self.checkAlertBatt_out()
			self.checkAleartTempBox_out()
			self.checkAlartHumBox_out()
			print("statusPumpOnBoxOut : ",self.statusPumpOnBoxOut)
			print("upload Boxout to Blynk")
			self.statusBoxoutblynk = False
		
	def gettimeformLocaltime(self):
		current_time = datetime.datetime.now()

		if current_time >= self.next_time:
            # หรือทำสิ่งที่คุณต้องการทำทุก 1 วินาทีตรงนี้
			timeis = time.localtime()
            #self.localimepi = time.strftime('%A %d %B %Y, %H:%M:%S',timeis)
			self.datelocal = time.strftime('%A')
			self.hourandmin = str(timeis.tm_hour)+":"+str(timeis.tm_min)+":"+str(timeis.tm_sec)
            #print(self.localimepi)
			print(self.datelocal)
			print(self.hourandmin)
			self.next_time = current_time + datetime.timedelta(seconds=1)
	def checkAlarmOpenpump(self):
		current_time= datetime.datetime.now()
		if current_time >= self.next_time1:
            # หรือทำสิ่งที่คุณต้องการทำทุก 1 วินาทีตรงนี้
			self.day_and_minute_one = str(self.sethourone)+":"+str(self.setminuteone)+":0"
			self.day_and_minute_two = str(self.sethourtwo)+":"+str(self.setminutetwo)+":0"
			self.day_and_minute_three = str(self.sethourthree)+":"+str(self.setminutethree)+":0"
			self.day_and_minute_four = str(self.sethourfour)+":"+str(self.setminutefour)+":0"
			self.day_and_minute_five = str(self.sethourfive)+":"+str(self.setminutefive)+":0"
			self.day_and_minute_six = str(self.sethoursix)+":"+str(self.setminutesix)+":0"
			print("Test "+self.datelocal)
			if self.setswitchrangeone == 1:
				if self.setmonday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_one ): 
						print("Mon ONE")
						self.setStatusPump(1)
						box_out.sync_virtual(19)
						self.setwaitpump = self.setwaitpumpone
						print(self.setwaitpump)
					else:    
						print("No Time ONE")
				elif self.setsunday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_one ): 
						print("Sun ONE")
						self.setStatusPump(1)
						box_out.sync_virtual(19)
						self.setwaitpump = self.setwaitpumpone
						print(self.setwaitpump)
					else:    
						print("No Time ONE")
				elif self.settuesday == self.datelocal:
					print(self.settuesday+"=="+self.datelocal)
					print(self.hourandmin+"=="+self.day_and_minute_one)
					if(self.hourandmin == self.day_and_minute_one ): 
						print("Tue ONE")
						self.setStatusPump(1)
						box_out.sync_virtual(19)
						self.setwaitpump = self.setwaitpumpone
						print(self.setwaitpump)
					else:    
						print("No Time ONE")
				elif self.setwednesday == self.datelocal:
					print(self.setwednesday+"=="+self.datelocal)
					print(self.hourandmin+"=="+self.day_and_minute_one)
					if(self.hourandmin == self.day_and_minute_one ): 
						print("Wed ONE")
						self.setStatusPump(1)
						box_out.sync_virtual(19)
						self.setwaitpump = self.setwaitpumpone
						print(self.setwaitpump)
					else:    
						print("No Time ONE")
				elif self.setthursday == self.datelocal:
					print(self.setthursday+"=="+self.datelocal)
					print(self.hourandmin+"=="+self.day_and_minute_one)
					if(self.hourandmin == self.day_and_minute_one ): 
						print("Thr ONE")
						self.setStatusPump(1)
						box_out.sync_virtual(19)
						self.setwaitpump = self.setwaitpumpone
						print(self.setwaitpump)
					else:    
						print("No Time ONE")
				elif self.setfriday == self.datelocal:
					print(self.setfriday+"=="+self.datelocal)
					print(self.hourandmin+"=="+self.day_and_minute_one)
					if(self.hourandmin == self.day_and_minute_one ): 
						print("Fri ONE")
						self.setStatusPump(1)
						box_out.sync_virtual(19)
						self.setwaitpump = self.setwaitpumpone
						print(self.setwaitpump)
					else:    
						print("No Time ONE")
				elif self.setsaturday == self.datelocal:
					print(self.setsaturday+"=="+self.datelocal)
					print(self.hourandmin+"=="+self.day_and_minute_one)
					if(self.hourandmin == self.day_and_minute_one ): 
						print("Sat ONE")
						self.setStatusPump(1)
						box_out.sync_virtual(19)
						self.setwaitpump = self.setwaitpumpone
						print(self.setwaitpump)
					else:    
						print("No Time ONE")
				else:
					print("No ONE")
			if self.setswitchrangetwo == 1:
				if self.setmonday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_two ): 
						print("Mon TWO")
						self.setStatusPump(1)
						box_out.sync_virtual(36)
						self.setwaitpump = self.setwaitpumptwo
						print(self.setwaitpump)
					else:    
						print("No Time TWO")
				elif self.setsunday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_two ): 
						print("Sun TWO")
						self.setStatusPump(1)
						box_out.sync_virtual(36)
						self.setwaitpump = self.setwaitpumptwo
						print(self.setwaitpump)
					else:    
						print("No Time TWO")
				elif self.settuesday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_two ): 
						print("Tue TWO")
						self.setStatusPump(1)
						box_out.sync_virtual(36)
						self.setwaitpump = self.setwaitpumptwo
						print(self.setwaitpump)
					else:    
						print("No Time TWO")
				elif self.setwednesday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_two ): 
						print("Wed TWO")
						self.setStatusPump(1)
						box_out.sync_virtual(36)
						self.setwaitpump = self.setwaitpumptwo
						print(self.setwaitpump)
					else:    
						print("No Time TWO")
				elif self.setthursday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_two ): 
						print("Thr TWO")
						self.setStatusPump(1)
						box_out.sync_virtual(36)
						self.setwaitpump = self.setwaitpumptwo
						print(self.setwaitpump)
					else:    
						print("No Time TWO")
				elif self.setfriday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_two ): 
						print("Fri TWO")
						self.setStatusPump(1)
						box_out.sync_virtual(36)
						self.setwaitpump = self.setwaitpumptwo
						print(self.setwaitpump)
					else:    
						print("No Time TWO")
				elif self.setsaturday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_two ): 
						print("Sat TWO")
						self.setStatusPump(1)
						box_out.sync_virtual(36)
						self.setwaitpump = self.setwaitpumptwo
						print(self.setwaitpump)
					else:    
						print("No Time TWO")
				else:
					print("No TWO")
			if self.setswitchrangethree == 1:
				if self.setmonday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_three ): 
						print("Mon THREE")
						self.setStatusPump(1)
						box_out.sync_virtual(37)
						self.setwaitpump = self.setwaitpumpthree
						print(self.setwaitpump)
					else:    
						print("No Time THREE")
				elif self.setsunday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_three ): 
						print("Sun THREE")
						self.setStatusPump(1)
						box_out.sync_virtual(37)
						self.setwaitpump = self.setwaitpumpthree
						print(self.setwaitpump)
					else:    
						print("No Time THREE")
				elif self.settuesday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_three ): 
						print("Tue THREE")
						self.setStatusPump(1)
						box_out.sync_virtual(37)
						self.setwaitpump = self.setwaitpumpthree
						print(self.setwaitpump)
					else:    
						print("No Time THREE")
				elif self.setwednesday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_three ): 
						print("Wed THREE")
						self.setStatusPump(1)
						box_out.sync_virtual(37)
						self.setwaitpump = self.setwaitpumpthree
						print(self.setwaitpump)
					else:    
						print("No Time THREE")
				elif self.setthursday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_three ): 
						print("Thr THREE")
						self.setStatusPump(1)
						box_out.sync_virtual(37)
						self.setwaitpump = self.setwaitpumpthree
						print(self.setwaitpump)
					else:    
						print("No Time THREE")
				elif self.setfriday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_three ): 
						print("Fri THREE")
						self.setStatusPump(1)
						box_out.sync_virtual(37)
						self.setwaitpump = self.setwaitpumpthree
						print(self.setwaitpump)
					else:    
						print("No Time THREE")
				elif self.setsaturday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_three ): 
						print("Sat THREE")
						self.setStatusPump(1)
						box_out.sync_virtual(37)
						self.setwaitpump = self.setwaitpumpthree
						print(self.setwaitpump)
					else:    
						print("No Time THREE")
				else:
					print("No THREE")
			if self.setswitchrangefour == 1:
				if self.setmonday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_four ): 
						print("Mon FOUR")
						self.setStatusPump(1)
						box_out.sync_virtual(38)
						self.setwaitpump = self.setwaitpumpfour
						print(self.setwaitpump)
					else:    
						print("No Time FOUR")
				elif self.setsunday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_four ): 
						print("Sun FOUR")
						self.setStatusPump(1)
						box_out.sync_virtual(38)
						self.setwaitpump = self.setwaitpumpfour
						print(self.setwaitpump)
					else:    
						print("No Time FOUR")
				elif self.settuesday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_four ): 
						print("Tue FOUR")
						self.setStatusPump(1)
						box_out.sync_virtual(38)
						self.setwaitpump = self.setwaitpumpfour
						print(self.setwaitpump)
					else:    
						print("No Time FOUR")
				elif self.setwednesday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_four ): 
						print("Wed FOUR")
						self.setStatusPump(1)
						box_out.sync_virtual(38)
						self.setwaitpump = self.setwaitpumpfour
						print(self.setwaitpump)
					else:    
						print("No Time FOUR")
				elif self.setthursday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_four ): 
						print("Thr FOUR")
						self.setStatusPump(1)
						box_out.sync_virtual(38)
						self.setwaitpump = self.setwaitpumpfour
						print(self.setwaitpump)
					else:    
						print("No Time FOUR")
				elif self.setfriday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_four ): 
						print("Fri FOUR")
						self.setStatusPump(1)
						box_out.sync_virtual(38)
						self.setwaitpump = self.setwaitpumpfour
						print(self.setwaitpump)
					else:    
						print("No Time FOUR")
				elif self.setsaturday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_four ): 
						print("Sat FOUR")
						self.setStatusPump(1)
						box_out.sync_virtual(38)
						self.setwaitpump = self.setwaitpumpfour
						print(self.setwaitpump)
					else:    
						print("No Time FOUR")
				else:
					print("No FOUR")
			if self.setswitchrangefive == 1:
				if self.setmonday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_five ): 
						print("Mon FIVE")
						self.setStatusPump(1)
						box_out.sync_virtual(39)
						self.setwaitpump = self.setwaitpumpfive
						print(self.setwaitpump)
					else:    
						print("No Time FIVE")
				elif self.setsunday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_five ): 
						print("Sun FIVE")
						self.setStatusPump(1)
						box_out.sync_virtual(39)
						self.setwaitpump = self.setwaitpumpfive
						print(self.setwaitpump)
					else:    
						print("No Time FIVE")
				elif self.settuesday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_five ): 
						print("Tue FIVE")
						self.setStatusPump(1)
						box_out.sync_virtual(39)
						self.setwaitpump = self.setwaitpumpfive
						print(self.setwaitpump)
					else:    
						print("No Time FIVE")
				elif self.setwednesday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_five ): 
						print("Wed FIVE")
						self.setStatusPump(1)
						box_out.sync_virtual(39)
						self.setwaitpump = self.setwaitpumpfive
						print(self.setwaitpump)
					else:    
						print("No Time FIVE")
				elif self.setthursday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_five ): 
						print("Thr FIVE")
						self.setStatusPump(1)
						box_out.sync_virtual(39)
						self.setwaitpump = self.setwaitpumpfive
						print(self.setwaitpump)
					else:    
						print("No Time FIVE")
				elif self.setfriday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_five ): 
						print("Fri FIVE")
						self.setStatusPump(1)
						box_out.sync_virtual(39)
						self.setwaitpump = self.setwaitpumpfive
						print(self.setwaitpump)
					else:    
						print("No Time FIVE")
				elif self.setsaturday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_five ): 
						print("Sat FIVE")
						self.setStatusPump(1)
						box_out.sync_virtual(39)
						self.setwaitpump = self.setwaitpumpfive
						print(self.setwaitpump)
					else:    
						print("No Time FIVE")
				else:
					print("No FIVE")
			if self.setswitchrangesix == 1:
				if self.setmonday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_six ): 
						print("Mon SIX")
						self.setStatusPump(1)
						box_out.sync_virtual(40)
						self.setwaitpump = self.setwaitpumpsix
						print(self.setwaitpump)
					else:    
						print("No Time SIX")
				elif self.setsunday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_six ): 
						print("Sun SIX")
						self.setStatusPump(1)
						box_out.sync_virtual(40)
						self.setwaitpump = self.setwaitpumpsix
						print(self.setwaitpump)
					else:    
						print("No Time SIX")
				elif self.settuesday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_six ): 
						print("Tue SIX")
						self.setStatusPump(1)
						box_out.sync_virtual(40)
						self.setwaitpump = self.setwaitpumpsix
						print(self.setwaitpump)
					else:    
						print("No Time SIX")
				elif self.setwednesday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_six ): 
						print("Wed SIX")
						self.setStatusPump(1)
						box_out.sync_virtual(40)
						self.setwaitpump = self.setwaitpumpsix
						print(self.setwaitpump)
					else:    
						print("No Time SIX")
				elif self.setthursday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_six ): 
						print("Thr SIX")
						self.setStatusPump(1)
						box_out.sync_virtual(40)
						self.setwaitpump = self.setwaitpumpsix
						print(self.setwaitpump)
					else:    
						print("No Time SIX")
				elif self.setfriday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_six ): 
						print("Fri SIX")
						self.setStatusPump(1)
						box_out.sync_virtual(40)
						self.setwaitpump = self.setwaitpumpsix
						print(self.setwaitpump)
					else:    
						print("No Time SIX")
				elif self.setsaturday == self.datelocal:
					if(self.hourandmin == self.day_and_minute_six ): 
						print("Sat SIX")
						self.setStatusPump(1)
						box_out.sync_virtual(40)
						self.setwaitpump = self.setwaitpumpsix
						print(self.setwaitpump)
					else:    
						print("No Time SIX")
				else:
					print("No SIX")  
			self.next_time1 = current_time + datetime.timedelta(seconds=1)
	
	def updateTimeLoRaConnect(self, box) :
		if box == "in" :
			self.time_alert_receive_in = datetime.datetime.now() + datetime.timedelta(minutes=10)
			box_in.virtual_write(35,1)
			box_in.virtual_write(36,0)
			
		elif box == "out" :
			self.time_alert_receive_out = datetime.datetime.now() + datetime.timedelta(minutes=10)
			box_out.virtual_write(53,1)
			box_out.virtual_write(54,0)
			
	def set_LoRa_no_connect(self, box):
		if box == "in":
			box_in.virtual_write(35,0)
			box_in.virtual_write(36,1)
			box_in.log_event("lora_not_connect", "ติดต่อ กล่องเซนเซอร์ไม่ได้")
		elif box == "out" :
			box_out.virtual_write(53,0)
			box_out.virtual_write(54,1)
			box_out.log_event("lora_not_connect", "ติดต่อ กล่องเซนเซอร์ไม่ได้")
		
	def start(self):
		self.reset_ptr_rx()
		self.set_mode(MODE.RXCONT)
		while True:
			try:
				self.setupMode()
				"""
				box_out.log_event("lora_not_connect" , "BattLow")
				box_out.log_event("batt_alarm" , "BattLow")
				box_out.log_event("temp_alarm" , "BattLow")
				box_out.log_event("humi_alarm" , "BattLow")
				"""
				self.current_time = datetime.datetime.now()
				self.setupMode()
				self.gettimeformLocaltime()
				self.checkAlarmOpenpump()
				if self.current_time >= self.time_alert_receive_in:
					self.set_LoRa_no_connect("in")
			
				if self.current_time >= self.time_alert_receive_out:
					self.set_LoRa_no_connect("out")
			
				if self.statusBox == True:
					sleep(1)
					self.send_data()
			except Exception as e:
				current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				print("System Error : ",e)
				with open('Log file/logfile_error.txt', 'a') as file:
					file.write('time : '+current_time_str)
					file.write(' error : '+str(e)+"\n")
					try:
					    box_in.connect()
					    box_out.connect()
					except:
					    pass
				continue
				
	def send_data_to_box_out(self,status):
		if status == True:
			#addr_gateway + addr_boxout + status data + status hard reset + status pump + time to pump active
			self.sumdataboxout = self.address_gateway+","+self.address_out+",0,"+str(self.hardresetboxout)+","+str(self.statusPump)+","+str(self.setwaitpump)
		else:
			self.sumdataboxout = self.address_gateway+","+self.address_out+",0,"+str(self.hardresetboxout)+","+str(self.statusPump)+","+str(self.setwaitpump)
		print("send to Boxout  "  +self.sumdataboxout)
		print("-------send Pi to Boxout-------")
		self.write_payload(self.sumdataboxout)
		self.set_mode(MODE.TX)
		self.clear_irq_flags(TxDone=1)
		sleep(0.5)
		self.set_mode(MODE.STDBY)
		self.set_mode(MODE.RXCONT)
		self.statusBoxout = False
		self.statusBox = False
		self.statusBoxoutblynk = True
	
	def checkStatusPump(self):
		print("self.statuspump : ",self.statusPump)
		if self.huminsoil < self.humidityPumpStart and self.huminsoil != 0:
			self.statePump = 2
			
		elif self.statusPump == 1:
			self.statePump = 1
		
		elif self.statusPumpOnWeb == 3 :
			self.statusPump = 3
			
		elif self.statusPumpOnBoxOut == 1 :
			self.statePump = 3
			
		elif self.statusPumpOnWeb == 4 or (self.huminsoil > self.humidityPumpStart and self.huminsoil == 0) or self.statusPumpOnBoxOut == 0: 
			self.statePump = 0;
	"""
		if self.huminsoil > self.humidityPumpStart or self.huminsoil == 0:
			self.statusPump = 0
		
		if self.statusPumpOnWeb == 3:
			self.statusPumpOnWeb = 0
			self.statusPump = 3
		
		if self.statusPumpOnWeb == 4 :
			self.statusPumpOnWeb = 0
			self.statusPump = 4
			
		if self.statusPumpOnBoxOut == 3 :
			#self.statusPump = 3
			self.statusPump = 0
			box_out.virtual_write(41 , 3)
			
		if self.statusPumpOnBoxOut == 4 :
			#self.statusPump = 4
			self.statusPump = 0
			box_out.virtual_write(41, 4)
			
		#if self.statusAC == 1 and  
	"""
	def send_data(self):
		print("statusBoxout : ",self.statusBoxout)
		if self.statusBoxin == True:
			print("humi_soil : ",self.humi_soil)
			print("humidityPumpStart : ",self.humidityPumpStart)
			if self.humi_soil < self.humidityPumpStart and self.humi_soil != 0 and self.pumpHumidity != 0:
				print("statusPump : ",self.statusPump)
				#sumdataboxin = addr_gateway + addr_boxin + status data + status hard reset
				self.sumdataboxin = self.address_gateway+","+self.address_in+",2,"+str(self.hardresetboxin)
				print("send to Boxin  "  +self.sumdataboxin)
				print("-------send Pi to Boxin-------")
				self.write_payload(self.sumdataboxin)
				self.set_mode(MODE.TX)
				self.clear_irq_flags(TxDone=1)
				sleep(0.5) 
				self.set_mode(MODE.STDBY)
				self.set_mode(MODE.RXCONT)
				self.statusBoxin = False
				self.statusBox = False
				self.statusBoxinblynk = True
				self.hardresetboxin=0
				self.updateBlynk()
				#print(bytes(send_payload).decode("utf-8", "ignore"))
                #sleep(0.1)
                #print("Values sent to New Blynk Server!")
			else :
				self.sumdataboxin = self.address_gateway+","+self.address_in+",0,"+str(self.hardresetboxin)
				print("send to Boxin  "  +self.sumdataboxin)
				print("-------send Pi to Boxin-------")
				self.write_payload(self.sumdataboxin)
				self.set_mode(MODE.TX)
				self.clear_irq_flags(TxDone=1)
				sleep(0.5) 
				self.set_mode(MODE.STDBY)
				self.set_mode(MODE.RXCONT)
				self.statusBoxin = False
				self.statusBox = False
				self.statusBoxinblynk = True
				self.hardresetboxin=0
				self.updateBlynk()
		elif self.statusBoxinfail == True:
				print("-------send Pi to Boxin-------")
				self.sumdataboxin = self.address_gateway+","+self.address_in+",1,"+str(self.hardresetboxin)
				self.write_payload(self.sumdataboxin)
				self.set_mode(MODE.TX)  
				self.clear_irq_flags(TxDone=1)
				sleep(0.5) 
				self.set_mode(MODE.STDBY)
				self.statusBoxinfail = False
				self.statusBox = False
				#self.hardresetboxin=0
                
		if self.statusBoxout == True:
			#self.checkStatusPump()
			print("Status pump : ", self.statusPump)
			#print("status pump : ", self.setwaitpump)
			self.sumdataboxout = self.address_gateway+","+self.address_out+",0,"+str(self.hardresetboxout)+","+str(self.statusPump)+","+str(self.setwaitpump)
			print("humisiol : ",self.humi_soil)
			print("humidityPumpStart : ",self.humidityPumpStart)
			if  self.humi_soil < self.humidityPumpStart and self.humi_soil != 0 and self.pumpHumidity != 0	:
				self.statusPump	= 2
				self.pumpWorkByHumiDone = False
				print("statusPump : ",self.statusPump)
				#sumdataboxin = addr_gateway + addr_boxout + status data + status hard reset + status pump + time to pump active
				self.sumdataboxout = self.address_gateway+","+self.address_out+",0,"+str(self.hardresetboxout)+","+str(self.statusPump)+","+str(self.setwaitpump)
			elif  self.humi_soil > self.humidityPumpStart and self.pumpHumidity != 0 and self.pumpWorkByHumiDone == False:
				self.statusPump	= 4	
				self.pumpWorkByHumiDone = True
				print("statusPump : ",self.statusPump)
				#sumdataboxin = addr_gateway + addr_boxout + status data + status hard reset + status pump + time to pump active
				self.sumdataboxout = self.address_gateway+","+self.address_out+",0,"+str(self.hardresetboxout)+","+str(self.statusPump)+","+str(self.setwaitpump)
			else :
				print("statusPump : ",self.statusPump)
				#sumdataboxin = addr_gateway + addr_boxout + status data + status hard reset + status pump + time to pump active
				self.sumdataboxout = self.address_gateway+","+self.address_out+",0,"+str(self.hardresetboxout)+","+str(self.statusPump)+","+str(self.setwaitpump)
			
			print("send to Boxout  "  +self.sumdataboxout)
			print("-------send Pi to Boxout-------")
			print("state pump : ", self.statePump)
			self.write_payload(self.sumdataboxout)
			self.set_mode(MODE.TX)
			self.clear_irq_flags(TxDone=1)
			sleep(0.5) 
			self.set_mode(MODE.STDBY)
			self.set_mode(MODE.RXCONT)
			self.statusBoxout = False
			self.statusBox = False
			self.statusBoxoutblynk = True
			self.hardresetboxout=0
			self.statusPump = 0
			print("Status pump : ", self.statusPump)
			self.setwaitpump= 0
			#f self.statusPumpOnBoxOut == 0 and self.statusPumpOnWeb == 3 :
			print("update blynkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
			self.updateBlynk()
			#print(bytes(send_payload).decode("utf-8", "ignore"))
			#sleep(0.1
			#print("Values sent to New Blynk Server!")
		elif self.statusBoxoutfail == True:
				print("-------send Pi to Boxout-------")
				self.sumdataboxout = self.address_gateway+","+self.address_out+",1,"+str(self.hardresetboxout)+","+str(self.statusPump)+","+str(self.setwaitpump)
				self.write_payload(self.sumdataboxout)
				self.set_mode(MODE.TX)  
				self.clear_irq_flags(TxDone=1)
				sleep(0.5) 
				self.set_mode(MODE.STDBY)
				self.set_mode(MODE.RXCONT)
				self.statusBoxoutfail = False
				self.statusBox = False
				#self.hardresetboxin=0
            
	def on_rx_done(self):
		print("\nRxDone")
		self.clear_irq_flags(RxDone=1)
		payload = self.read_payload(nocheck=True)
		print("payload:", payload)
        
        
		if str(payload[0]) == self.address_in and str(payload[1]) == self.address_gateway :
			if payload is not None:
				self.addressNode_rx = payload[0]
				self.addressGateway_rx = payload[1]
				payload_without_first_three = payload[2:]
				payload_as_str = [str(item) for item in payload]
				self.statusBox = True
				
				
				self.receivedboxin_data  = ''.join([chr(num) for num in payload_without_first_three])
				print("Received Boxin (as string):", self.receivedboxin_data)
				data_list = self.receivedboxin_data.split(',')
				current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				with open('logfile_boxin 12 - 3.txt', 'a') as file:
					file.write('\n'+current_time_str)
					file.write('\nReceive as byte		: '+','.join(payload_as_str))
					file.write('\nReceive as String	: '+self.receivedboxin_data)
					file.write('\nRSSI 				: '+str(self.get_pkt_rssi_value()))
					file.write('\nSNR  				: '+str(self.get_pkt_snr_value()))
				try:
					self.tempinbox_in = float(data_list[0])
					self.tempinair = float(data_list[1])  
					self.huminair = float(data_list[2])
					self.huminbox = float(data_list[3])  
					self.humi_soil = float(data_list[4])
					self.light = float(data_list[5])
					self.battery_boxin = float(data_list[6])
					self.battery_boxin = ((self.battery_boxin - 2.5) * (100 - 0)) / (4.2 - 2.5) + 0
					self.statusBox = True
					self.statusBoxin = True
					print("data box in correct")
					self.updateTimeLoRaConnect("in")
					#self.checkStatusPump();
					#self.send_data(self.address_in,0)
				except:
					self.statusBox = True
					self.statusBoxinfail = True
					print("data box in not correct")
					self.updateTimeLoRaConnect("in")
					#self.send_data(self.address_in,1)
				#finally:
				#	sleep(2)
                    
		elif str(payload[0]) == self.address_out and str(payload[1]) == self.address_gateway:
			if payload is not None:
				self.addressNode_rx = payload[0]
				self.addressGateway_rx = payload[1]
				payload_without_first_three = payload[2:]
				payload_as_str = [str(item) for item in payload]
				
				self.receivedboxout_data  = ''.join([chr(num) for num in payload_without_first_three])
				print("Received Boxout (as string):", self.receivedboxout_data)
				data_list = self.receivedboxout_data.split(',')
				current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				self.statusBox = True
				

				with open('logfile_boxout 12 - 3.txt', 'a') as file:
					file.write('\n'+current_time_str)
					file.write('\nReceive as byte		: '+','.join(payload_as_str))
					file.write('\nReceive as String	: '+self.receivedboxout_data)
					file.write('\nRSSI 				: '+str(self.get_pkt_rssi_value()))
					file.write('\nSNR  				: '+str(self.get_pkt_snr_value()))
				try:
					self.tempoutbox_out = float(data_list[0])
					self.humoutbox = float(data_list[1])
					self.ec = float(data_list[2])
					self.ph = float(data_list[3])
					self.statusPumpWorking = int(data_list[4])
					self.battery_boxout = float(data_list[5])
					self.battery_boxout = ((self.battery_boxout - 2.5) * (100 - 0)) / (4.2 - 2.5) + 0
					self.statusPumpOnBoxOut = int(data_list[6])
					if self.statusPumpOnBoxOut == 0 :
						self.statusPumpOnBoxOut = 4
					else :
						self.statusPumpOnBoxOut = 3
					
					print("statusPumpOnBoxOut : ",self.statusPumpOnBoxOut)
					
					self.statusBoxout = True
					print("box out receive true")
					self.updateTimeLoRaConnect("out")
					#self.checkStatusPump();
					#self.send_data(self.address_out,0)
					
				except Exception as e:
					#print(e)
					print("box out receive false")
					#self.send_data(self.address_out,1)
					self.statusBox = True
					self.statusBoxoutfail = True
					self.updateTimeLoRaConnect("out")
				#finally:
				#	sleep(1)
		else: print("----------don't care----------")
        
lora = LoRaGateway(verbose=True)
lora.set_mode(MODE.STDBY)

lora.set_pa_config(pa_select=1)
lora.set_freq(923.0)
try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
