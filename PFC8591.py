#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from smbus import SMBus
from datetime import datetime

#board pins
#pin 1=3v3
#pin 3=SDA
#pin 5=SCL
#pin 9=GND
#wartosci sa zwracane jako napiecie

class PFC8591:
	def __init__(self,debug):
		self.bus_i2c = 0
		self.Vref = 0
		self.address = 0
		self.port = 0
		self.value = 0.0
		self.debug = debug

	def SetOptions(self,options):
                opts = {}
		if(self.debug):
			print "%s [DEBUG]Otrzymane opcje %s" % (datetime.now(), options)
                try:
                        for option in options.split(";"):
                                option = option.split("=")
                                opts[ option[0] ] = option[1]
                        self.bus_i2c = SMBus(int(opts['bus']))
                        self.Vref = float(opts['Vref'])
                        self.address = int(opts['address'])
                        self.port = int(opts['port'])
		except:
			if(self.debug):
				print "%s [DEBUG]Ustawianie opcji zakończyło się błędnie, możliwe błędne opcje lub czujnik nie działa" % datetime.now()
			return False
		if(self.debug):
			print "%s [DEBUG]Ustawianie opcji zakończyło się powodzeniem bus_i2c=%s, address=%s, port=%s, Vref=%s" % (datetime.now(), self.bus_i2c, self.address, self.port, self.Vref)
		return True
	
	def ReadValue(self):
		if(self.debug):
			print "%s [DEBUG]Odczyt wartości dla port=%s" % (datetime.now(), self.port)
		try:
			self.bus_i2c.write_byte(self.address, self.port)
			time.sleep(0.4)
			self.bus_i2c.read_byte(self.address)
			self.bus_i2c.read_byte(self.address)
			Ain = float( self.bus_i2c.read_byte(self.address) )
			self.value = ( Ain * self.Vref ) / float( 255 ) 
		except:
			if(self.debug):
				print "%s [DEBUG]Błąd odczytu wartości" % datetime.now()
			return False
		if(self.debug):
			print "%s [DEBUG]Odczyt poprawny, wartość=%s" % (datetime.now(), self.value)
        	return self.value 

#pf = PFC8591(debug=1)
#pf.SetOptions("bus=1;address=72;port=0;Vref=3.3")
#print pf.ReadValue()
#pf.SetOptions("bus=1;address=72;port=1;Vref=3.3")
#print pf.ReadValue()
#pf.SetOptions("bus=1;address=72;port=2;Vref=3.3")
#print pf.ReadValue()
#pf.SetOptions("bus=1;address=72;port=3;Vref=3.3")
#print pf.ReadValue()

