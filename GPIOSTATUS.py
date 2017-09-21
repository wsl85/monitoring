#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO
from datetime import datetime

#board pins
#pin 11=gpio17
#pin 12=gpio18
#pin 13=gpio27
#pin 15=gpio22

#GPIO.BOARD = 10
#GPIO.BCM = 11
#GPIO.OUT = 0
#GPIO.IN = 1


class GPIOSTATUS:
	def __init__(self,debug):
		self.debug = debug
		self.gpio_mode = GPIO.BCM
		self.gpio_setup = 0
		GPIO.setwarnings(False)
		self.value = 0.0
		self.gpio = -1
	def SetOptions(self,options):
                opts = {}
		if(self.debug):
			print "%s [DEBUG]Otrzymane opcje %s" % (datetime.now(), options)
                try:
                        for option in options.split(";"):
                                option = option.split("=")
                                opts[ option[0] ] = option[1]
                        self.gpio = int(opts['gpio'])
			self.gpio_mode = int(opts['gpio_mode'])
			self.gpio_setup = int(opts['gpio_setup'])
			GPIO.setmode(self.gpio_mode)
			GPIO.setup(self.gpio,self.gpio_setup)
		except:
			if(self.debug):
				print "%s [DEBUG]Ustawianie opcji zakończyło się błędnie, możliwe błędne opcje lub czujnik nie działa" % datetime.now()
			return False
		if(self.debug):
			print "%s [DEBUG]Ustawianie opcji zakończyło się powodzeniem, gpio=%s" % (datetime.now(), self.gpio)
		return True
		
	def ReadValue(self):
                if(self.debug):
                        print "%s [DEBUG]Odczyt wartości dla gpio=%s" % (datetime.now(), self.gpio)
		try:
			if( self.gpio == -1 ):
				if(self.debug):
					print "%s [DEBUG]Nieobsługiwany numer gpio" % datetime.now()
				return False
			else:
				self.value = GPIO.input(self.gpio)
                except:
                        if(self.debug):
                                print "%s [DEBUG]Błąd odczytu wartości" % datetime.now()
                        return False
		if(self.debug):
			print "%s [DEBUG]Odczyt poprawny, wartość=%s" % (datetime.now(), self.value)
		return self.value


#g = GPIOSTATUS(1)
#g.SetOptions("gpio=17;gpio_mode=11;gpio_setup=0")
#print g.ReadValue()
