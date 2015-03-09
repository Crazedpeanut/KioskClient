'''
Author: John Kendall
Date: 18/12/14

Description: Reads from the hid raw device file. As a way of binding to a bar code scanner
            (Requires either root permissions or read permission of the hid raw device file)
'''
import time
import sys
import threading
import USBKey_converter as USBKey
import debug as dbug
import serial
import settings

buffersize = 16
TIME_WAIT = 0.2


class bcode(threading.Thread):
    
    def __init__(self, callback):
        self.callback = callback
        threading.Thread.__init__(self)

    def run(self):
        
        ser = serial.Serial(port=settings.SERIAL_DEVICE, baudrate=settings.SERIAL_DEVICE_BAUD)
        #ser.open()
        
        while(True):
            try: 

                f = open(settings.USB_DEVICE, 'r')
                    
                barcode = ""

                b = f.read(buffersize)
                dec = USBKey.usbkey_to_char(b[2])

                while(dec is not None):
                    barcode = barcode + str(dec)
                    b = f.read(buffersize)
                    dec = USBKey.usbkey_to_char(b[2])
                self.callback(barcode)
                time.sleep(TIME_WAIT)

            except Exception as e:
                dbug.debug(str(e))
            
            try:
                barcode = ser.readline()
                if(barcode is not None):
                    self.callback(barcode.decode('UTF-8'))
            except Exception as e:
                dbug.debug(str(e))
            
            time.sleep(0.2)

def print_barcode(barcode):
    sys.stdout.write(barcode)

def start_listening(callback):
    bcode_listen_thread = bcode(callback)
    bcode_listen_thread.start()

def main():
    thread = bcode(print_barcode)
    thread.start()

if(__name__ == "__main__"):
    main()
