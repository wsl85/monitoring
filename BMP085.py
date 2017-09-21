#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import Adafruit_BMP.BMP085
from datetime import datetime

#board pins
#pin 1=3v3
#pin 3=SDA
#pin 5=SCL
#pin 9=GND
#wartosc cisnienia jest zwracana w hPa
#wartosc teperatury jest zwracana w stopniach C

class BMP085():
	def __init__(self, debug):
		self.sensor = 0 #Adafruit_BMP.BMP085.BMP085(address=119)
		self.value = float(0)
		self.port = 1
		self.debug = debug

        def SetOptions(self, options):
                opts = {}
		if(self.debug):
			print "%s [DEBUG]Otrzymane opcje %s" % (datetime.now(), options)
                try:
                        for option in options.split(";"):
                                option = option.split("=")
                                opts[ option[0] ] = option[1]
                	bus_i2c = int(opts['bus'])
                	addr = int(opts['address'])
                	self.port = int(opts['port'])
                	self.sensor = Adafruit_BMP.BMP085.BMP085(busnum=bus_i2c, address=addr)
                except:
			if(self.debug):
				print "%s [DEBUG]Ustawianie opcji zakończyło się błędnie, możliwe błędne opcje lub czujnik nie działa" % datetime.now()
                        return False
                if(self.debug):
                        print "%s [DEBUG]Ustawianie opcji zakończyło się powodzeniem bus_i2c=%s, address=%s, port=%s" % (datetime.now(), bus_i2c, addr, self.port)
                return True

	def ReadValue(self):
                if(self.debug):
                        print "%s [DEBUG]Odczyt wartości dla port=%s" % (datetime.now(), self.port)
		try:
			if( self.port == 0 ):
				self.value = float(self.sensor.read_temperature())
			elif( self.port == 1 ):
				self.value = float(self.sensor.read_pressure() / 100.0 )
			else:
				if(self.debug):
					 print "%s [DEBUG]Nieobsługiwany numer portu" % datetime.now()
				return False
                except:
                        if(self.debug):
                                print "%s [DEBUG]Błąd odczytu wartości" % datetime.now()
                        return False
		if(self.debug):
			print "%s [DEBUG]Odczyt poprawny, wartość=%s" % (datetime.now(), self.value)
		return self.value


#bm = BMP085(debug=1)
#bm.SetOptions("bus=1;address=119;port=0")
#print bm.ReadValue()
#bm.SetOptions("bus=1;address=119;port=1")
#print bm.ReadValue()

