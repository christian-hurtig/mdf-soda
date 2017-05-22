#!/usr/bin/env python

import signal
import time
import sys

from pirc522 import RFID # https://github.com/ondryaso/pi-rc522/blob/master/examples/Read.py
import RPi.GPIO as GPIO  # https://sourceforge.net/projects/raspberry-gpio-python/
import mysql.connector   # https://dev.mysql.com/doc/connector-python/en/connector-python-examples.html

run = True
rdr = RFID()
util = rdr.util()
util.debug = True

GPIO.setmode(GPIO.BOARD)
inputPin = 11
outputPin = 12
GPIO.setup(inputPin, GPIO.IN, GPIO.PUD_DOWN) # Pull down correct?
GPIO.setup(outputPin, GPIO.OUT)

# TODO Fix db account information and permissions.
config = {
  'user': 'scott',
  'password': 'tiger',
  'host': '127.0.0.1',
  'database': 'employees',
  'raise_on_warnings': True,
  'use_pure': False,
}

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    GPIO.cleanup()
    sys.exit()

signal.signal(signal.SIGINT, end_read)


print("Starting")
while run:
    rdr.wait_for_tag()

    (error, data) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))

    (error, uid) = rdr.anticoll()
    if not error:
        # Card was detected and there were no errors
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        cursor.callproc('cardSwipe', (uid[0], uid[1], uid[2], uid[3]))
        results=mysql_cursor.fetchone()
        
        if result[0] >= 5:
            # Card was accepted and the account has more than 5 SEK, enable the butttons by setting output to high
            GPIO.output(outputPin, GPIO.HIGH)
            
            # Wait for 5000 ms for button press
            channel = GPIO.wait_for_edge(inputPin, GPIO_RISING, timeout=5000) 
            if channel is None:
                print('Timeout occurred')
            else:
                # Button was pressed and card should be charged. 
                cursor.callproc('buttonPressed', (uid[0], uid[1], uid[2], uid[3]))
        
        
        # Transaction complete, disable buttons and close db connection.
        cursor.close()
        cnx.close()
        GPIO.output(outputPin, GPIO.LOW)
       
       
time.sleep(1)
