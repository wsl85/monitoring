#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from datetime import datetime

class CPUTEMP:
	def __init__(self,debug):
		self.debug = debug
		self.value = 0.0
		self.file = "/sys/class/thermal/thermal_zone0/temp"
	def SetOptions(self,options):
		if(self.debug):
			print "%s [DEBUG]Ustawianie opcji zakończyło się powodzeniem" % datetime.now()
		return True
		
	def ReadValue(self):
                if(self.debug):
                        print "%s [DEBUG]Odczyt wartości dla temperatury procesora" % datetime.now()
		try:
			f = open(self.file, 'r')
			self.value = float(f.read()) / 1000
                except:
                        if(self.debug):
                                print "%s [DEBUG]Błąd odczytu wartości" % datetime.now()
                        return False
		if(self.debug):
			print "%s [DEBUG]Odczyt poprawny, wartość=%s" % (datetime.now(), self.value)
		return self.value


#g = CPUTEMP(1)
#g.SetOptions(1)
#print g.ReadValue()
