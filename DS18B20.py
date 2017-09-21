#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import Adafruit_BMP.BMP085
from datetime import datetime

#board pins
#pin 1=3v3
#pin 7=1wire
#pin 9=GND

#wartosc teperatury jest zwracana w stopniach C

class DS18B20():
	def __init__(self, debug):
		self.sensor = 0 
		self.value = float(0)
		self.debug = debug

        def SetOptions(self, options):
                opts = {}
		if(self.debug):
			print "%s [DEBUG]Otrzymane opcje %s" % (datetime.now(), options)
		try:
			for option in options.split(";"):
				option = option.split("=")
				opts[ option[0] ] = option[1]
			self.sensor = opts['address']
                except:
			if(self.debug):
				print "%s [DEBUG]Ustawianie opcji zakończyło się błędnie, możliwe błędne opcje lub czujnik nie działa" % datetime.now()
                        return False
                if(self.debug):
                        print "%s [DEBUG]Ustawianie opcji zakończyło się powodzeniem address=%s" % (datetime.now(), self.sensor)
                return True

	def ReadTempRaw(self):
		f = open(self.sensor, 'r')
		lines = f.readlines()
		f.close()
		return lines

	def ReadValue(self):
                if(self.debug):
                        print "%s [DEBUG]Odczyt wartości dla addresu=%s" % (datetime.now(), self.sensor)
		try:
			if( self.sensor == 0 ):
				if(self.debug):
					 print "%s [DEBUG]Nieobsługiwany numer portu" % datetime.now()
				return False
			else:
				lines = self.ReadTempRaw()
				while lines[0].strip()[-3:] != 'YES':
					time.sleep(0.2)
					lines = self.ReadTempRaw()
				equals_pos = lines[1].find('t=')
				if equals_pos != -1:
					temp_string = lines[1][equals_pos+2:]
					self.value = float(temp_string) / 1000.0
                except:
                        if(self.debug):
                                print "%s [DEBUG]Błąd odczytu wartości" % datetime.now()
                        return False
		if(self.debug):
			print "%s [DEBUG]Odczyt poprawny, wartość=%s" % (datetime.now(), self.value)
		return self.value


#temp = DS18B20(debug=1)
#temp.SetOptions("address=/sys/bus/w1/devices/28-021562abbdff/w1_slave")
#print temp.ReadValue()
#temp.SetOptions("address=/sys/bus/w1/devices/28-021573a445ff/w1_slave")
#print temp.ReadValue()

