#!/usr/bin/python
#--------------------------------------   
# This script reads data from a 
# MCP3008 ADC device using the SPI bus.
#
# Author : Matt Hawkins
# Date   : 25/122017
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

import spidev
import time
import os
import serial
import http.client
import urllib.request

key="VMPNSROP5WNJPZJ3"

SERIAL_PORT="/dev/ttyS0"

ser=serial.Serial(SERIAL_PORT,baudrate=9600,timeout=5)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places. 
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)  
  return volts
  
# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertTemp(data,places):
 
  temp = ((data * 330)/float(1023))-50
  temp = round(temp,places)
  return temp

def thermometer():
# Define sensor channels
#light_channel = 0
    temp_channel  = 0

    # Define delay between readings
    delay = 5

    while True:

      # Read the light sensor data
      #light_level = ReadChannel(light_channel)
      #light_volts = ConvertVolts(light_level,2)

      # Read the temperature sensor data
      temp_level = ReadChannel(temp_channel)
      temp_volts = ConvertVolts(temp_level,2)
      temp       = ConvertTemp(temp_level,2)       
          
      params=urllib.parse.urlencode({'field1':temp,'key':key})
      headers={"Content-typZZe":"application/x-www-form-urlencoded","Accept":"text/plain"}
      conn=http.client.HTTPConnection("api.thingspeak.com:80")
      try:
          conn.request("POST","/update",params,headers)
          response=conn.getresponse()
          print ("--------------------------------------------"  )
          #print("Light : {} ({}V)".format(light_level,light_volts))  
          print("Temp  : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))
          if(temp>20):
          
            ser.write(str.encode("ATD+918970736699;\r"))
            print("Dialling...")
            time.sleep(10)

            ser.write(str.encode("ATH\r"))
            print("HAnging up")
          
          print(response.status,response.reason)
          data=response.read()
          conn.close()
      except:
          print("Connection failed")
      break

      # Wait before repeating loop
      time.sleep(delay)

if __name__=="__main__":
    while True:
        thermometer()
