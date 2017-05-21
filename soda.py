#!/usr/bin/env python

import signal
import time
import sys

from pirc522 import RFID // https://github.com/ondryaso/pi-rc522/blob/master/examples/Read.py
import RPi.GPIO as GPIO  // https://sourceforge.net/projects/raspberry-gpio-python/
import mysql.connector   // https://dev.mysql.com/doc/connector-python/en/connector-python-examples.html

run = True
rdr = RFID()
util = rdr.util()
util.debug = True

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
        
        cnx = mysql.connector.connect(**config)
        cursor = conn.cursor()
 
        cursor.callproc('cardSwipe', (uid[0], uid[1], uid[2], uid[3]))
        results=mysql_cursor.fetchone()
        
        if result[0] >= 5:
            //CARD WAS ACCEPTED
            start = time.time()
            condition = True
            while condition:
            
                //CHECK GPIO FOR BUTTON PRESS, IF DETECTED THEN CHARGE ACCOUNT
                    cursor.callproc('buttonPressed', (uid[0], uid[1], uid[2], uid[3]))
                
                end = time.time()
                condition = end - start <= 5 // EXIT AFTER 5 SECONDS
        
        cursor.close()
        cnx.close()
       
       
time.sleep(1)
