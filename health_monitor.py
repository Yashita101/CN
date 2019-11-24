import spidev
import time
import os
from pulsesensor import Pulsesensor
import RPi.GPIO as GPIO
import serial
import sys
import http.client
import urllib.request

temp_key="VMPNSROP5WNJPZJ3"
pulse_rate_key="OV4UT8JRYDWS5B53"

SERIAL_PORT="/dev/ttyS0"

ser=serial.Serial(SERIAL_PORT,baudrate=9600,timeout=5)
p = Pulsesensor()
p.startAsyncBPM()
        
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000


def ReadChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

 
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)  
  return volts
  

def ConvertTemp(data,places):
  temp = ((data * 330)/float(1023))-50
  temp = round(temp,places)
  return temp

def health_monitor():

    temp_channel  = 0

    delay = 1

    while True:
        try:
            temp_level = ReadChannel(temp_channel)
            temp_volts = ConvertVolts(temp_level,2)
            temp       = ConvertTemp(temp_level,2)
            bpm = p.BPM
            
            params1=urllib.parse.urlencode({'field1':temp,'key':temp_key})
            headers1={"Content-typZZe":"application/x-www-form-urlencoded","Accept":"text/plain"}
            conn1=http.client.HTTPConnection("api.thingspeak.com:80")
            
            params2=urllib.parse.urlencode({'field1':bpm,'key':pulse_rate_key})
            headers2={"Content-typZZe":"application/x-www-form-urlencoded","Accept":"text/plain"}
            conn2=http.client.HTTPConnection("api.thingspeak.com:80")        

            conn1.request("POST","/update",params1,headers1)
            conn2.request("POST","/update",params2,headers2)
            response1=conn1.getresponse()
            response2=conn2.getresponse()
            if bpm > 0 or temp > 0:
                    print ("--------------------------------------------"  )
                    print("BPM: %d" % bpm)
                    print("Temp  : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))
                    if temp > 27 or bpm > 200:
                        ser.write(str.encode("ATD+918970736699;\r"))
                        print("Dialling...")
                        time.sleep(10)
                        ser.write(str.encode("ATH\r"))
                        print("HAnging up")
                    else:
                        print("No Heartbeat found %d" % bpm)
                        print("Temp  : {} ({}V) {} deg C".format(temp_level,temp_volts,temp)) 
                  
                    time.sleep(1)
            print(response1.status,response1.reason,response2.status,response2.reason)
            data1=response1.read()
            data2=response2.read()
        except InterruptedError as ie:
            p.stopAsyncBPM()
            conn.close()
        except ConnectionError as ce:
            print("Connection failed",ce)
        except KeyboardInterrupt as ki:
            print(ki)
            exit()
        break
        time.sleep(delay)
    
if __name__=="__main__":
    while True:
        health_monitor()
'''
SERIAL_PORT="/dev/ttyS0"
ser=serial.Serial(SERIAL_PORT,baudrate=9600,timeout=5)

ser.write(str.encode("ATD+918970736699;\r"))
print("Dialling...")
time.sleep(10)

ser.write(str.encode("ATH\r"))
print("HAnging up")

ser.write(str.encode('AT+CMGF=1\r'))
print("text mode enabled")
time.sleep(3)
ser.write(str.encode('AT+CMGS="+918970736699"\r'))
msg="hello"
time.sleep(3)
ser.write(str.encode(msg+chr(26)))
time.sleep(3)
print("message sent")'''