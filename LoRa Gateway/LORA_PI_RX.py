from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD

BOARD.setup()

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        
    def send_data_success(self):
        #self.write_payload("data correct")
        #self.set_mode(MODE.TX)
        #self.clear_irq_flags(TxDone=1)
        #print("Sending data")
        self.write_payload("data correct")
        self.set_mode(MODE.TX)
        print("Sending data")
    
    def send_data_error(self):
        print("Sending data")
        self.write_payload("data uncorrect")
        self.set_mode(MODE.TX)
        
    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(.5)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.flush()
            
    def on_rx_done(self):
        print("\nReceived: ")
        self.clear_irq_flags(RxDone=1)
        SNR = self.get_pkt_snr_value()
        rssi = self.get_pkt_rssi_value()
        payload = self.read_payload(nocheck=True)
        print(bytes(payload).decode("utf-8",'ignore'))
        print("RSSI = ",rssi)
        print("SNR = ",SNR)
        self.send_data_success()
        #self.set_mode(MODE.TX)
        #self.clear_irq_flags(TxDone=1)
        #self.write_payload("data correct")
        #self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT) 

lora = LoRaRcvCont(verbose=False)
lora.set_mode(MODE.STDBY)

#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm

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
