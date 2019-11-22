from pulsesensor import Pulsesensor
import time
import serial

SERIAL_PORT="/dev/ttyS0"

ser=serial.Serial(SERIAL_PORT,baudrate=9600,timeout=5)

p = Pulsesensor()
p.startAsyncBPM()

try:
    while True:
        bpm = p.BPM
        if bpm > 0:
            print("BPM: %d" % bpm)
            if bpm>100:
                ser.write(str.encode("ATD+918970736699;\r"))
                print("Dialling...")
                time.sleep(5)
                ser.write(str.encode("ATH\r"))
                print("HAnging up")

        else:
            print("No Heartbeat found")
        time.sleep(1)
except:
    p.stopAsyncBPM()
