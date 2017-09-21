#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO
import MySQLdb
from datetime import datetime

ENABLE = 1
DISABLE = 0
Vref = 3.3

DB_config = {'host': 'localhost',       # your host, usually localhost
             'user': 'monitoring',      # your username
             'passwd': 'monitoring',    # your password
             'db': 'monitoring1'}        # name of the data base

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#numery wyjsc gpio
GPIO_OUT1 = 17
GPIO_OUT2 = 27
GPIO_OUT3 = 22
#id sensorow
SENSOR_AIN0 = 3
SENSOR_AIN1 = 1
SENSOR_AIN2 = 6
SENSOR_AIN3 = 4

#poziomy wlaczenia wyjscia
OUT1_threshold = 0.8	
OUT2_threshold = 1.5   
OUT3_threshold = 1.5   

#czas dzialania wyjscia w sekundach
OUT1_RUNNING = 60
OUT2_RUNNING = 20
OUT3_RUNNING = 20

#ustawienie wyjsc
GPIO.setup(GPIO_OUT1, GPIO.OUT)
GPIO.output(GPIO_OUT1, DISABLE)
GPIO.setup(GPIO_OUT2, GPIO.OUT)
GPIO.output(GPIO_OUT2, DISABLE)
GPIO.setup(GPIO_OUT3, GPIO.OUT)
GPIO.output(GPIO_OUT3, DISABLE)

def GetValueFromDB(sensor):
	value = Vref
	db = MySQLdb.connect(**DB_config)
	buffor = db.cursor(MySQLdb.cursors.DictCursor)
	query = "SELECT AVG(vals.value) AS average FROM (SELECT value FROM `values` WHERE `sensor_id`=%s ORDER BY `id` DESC LIMIT 10) vals" % sensor
        buffor.execute(query)
	values = buffor.fetchone()
        if values is not None:
        	value = float(values['average'])
	db.close()
	return value

def OutputRunning(gpio,time_running):
	GPIO.output(gpio,ENABLE)
	time.sleep(time_running)
	GPIO.output(gpio,DISABLE)
	return

if __name__ == "__main__":
	value = GetValueFromDB(SENSOR_AIN0);
	print "%s [Podlewanie]srednia z ostatnich 10 wyników: %s" % (datetime.now(), value)
	if value > OUT1_threshold :
		OutputRunning(GPIO_OUT1, OUT1_RUNNING)

	
