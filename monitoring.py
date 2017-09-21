#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO
import MySQLdb
import PFC8591
import BMP085
import DS18B20
import GPIOSTATUS
import CPUTEMP
from datetime import date, datetime, timedelta

debug = 0                               # 1 - enable, 0 -  disable
ENABLE = 1
DISABLE = 0

Sleep_time = 10                         # seconds

DB_config = {'host': 'localhost',       # your host, usually localhost
             'user': 'monitoring',      # your username
             'passwd': 'monitoring',    # your password
             'db': 'monitoring1'}        # name of the data base

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_LM393 = 18 
GPIO.setup(GPIO_LM393, GPIO.OUT)
GPIO.output(GPIO_LM393, DISABLE)

class Monitoring():
	def __init__(self):
		self.db = 0
		self.sensors = 0
		self.sensor = 0
		self.value_new = 0

	def ConnectDB(self,DB_config,debug):
		if(debug):
			print ( "%s [DEBUG]Łączenie się z hostem=%s do bazy %s z użytkownikem %s, hasłem %s" %
					( datetime.now(),DB_config['host'], DB_config['db'],
					DB_config['user'], DB_config['passwd'] ) )
		try:
			self.db = MySQLdb.connect(**DB_config)
		except:
			if(debug):
				print "%s [DEBUG]Błąd połączenia z bazą" % datetime.now()
			return 0
		if(debug):
			print "%s [DEBUG]Połączono się z bazą" % datetime.now()
		return 1

	def CloseDB(self):
		self.db.close()

	def PrintSensors(self):
		print self.sensors

        def PrintSensor(self):
                print self.sensor
	
	def PrintNewValue(self):
		print self.value_new
	
	def GetSensors(self,debug):
		query = "SELECT * FROM `sensors` WHERE `enable`=1"
		if(debug):
			print "%s [DEBUG]Wykonuję zapytanie %s" % (datetime.now(), query)
		try:
			buffor = self.db.cursor(MySQLdb.cursors.DictCursor)
			buffor.execute(query)
			sensors = buffor.fetchall()
		except:
                        if(debug):
                                print "%s [DEBUG]Błąd wykonania zapytania" % datetime.now()
                        return 0
		if(debug):
			print "%s [DEBUG]Zapytanie wykonano poprawnie" % datetime.now()
		return sensors

	def SaveValueIsDifferent(self, id, value, delta, debug):
		value_old = 0
		DB_insert_values = ("INSERT INTO `values` "
				"(`id`, `sensor_id`, `time`, `value`) "
				"VALUES (NULL, %s, '%s', %s)")
		try:
			buffor = self.db.cursor(MySQLdb.cursors.DictCursor)
			#pobranie ostatniej wartosci danego czujnika
			query = "SELECT * FROM `values` WHERE `sensor_id`=%s ORDER BY `id` DESC LIMIT 1" % id
                	buffor.execute(query)
			values = buffor.fetchone()
                        if values is not None:
                                value_old = float(values['value'])
		
			if abs(value - value_old) >= delta:
				#zapisanie nowej wartosci       
                                query = DB_insert_values % (id, datetime.now(), value )
                                buffor.execute( query )

			self.db.commit()
		except:
			if(debug):
				print "%s [DEBUG]Błąd przy zapisie wartości do bazy" % datetime.now()
			self.db.rollback()
			return False	
		return True

	def SaveValue(self, id, value, debug):		
                DB_insert_values = ("INSERT INTO `values` "
                                "(`id`, `sensor_id`, `time`, `value`) "
                                "VALUES (NULL, %s, '%s', %s)")
		query = DB_insert_values % (id, datetime.now(), value )
		if(debug):
			print "%s [DEBUG]Wykonuję zapytanie %s" % (datetime.now(), query)
		try:
                	#zapisanie nowej wartosci
			buffor = self.db.cursor(MySQLdb.cursors.DictCursor)
			buffor.execute(query)
			self.db.commit()
                except:
			if(debug):
                		print "%s [DEBUG]Błąd wykonywania zapytania " % datetime.now() 
			self.db.rollback()
                        return False
                if(debug):
			print "%s [DEBUG]Zapytanie wykonano poprawnie" % datetime.now()     		
                return True


if __name__ == "__main__":
	Monitoring = Monitoring()
	while(1):
		if( Monitoring.ConnectDB(DB_config,debug)):
			#uruchomienie LM393
			GPIO.output(GPIO_LM393, ENABLE)
			sensors = Monitoring.GetSensors(debug)
			if( sensors ):
				for sensor in sensors:
					if(debug):
						print "%s [DEBUG]Obsługa czyjnika %s" % (datetime.now(),sensor['name'])
					if sensor['model'] == "PFC8591":
						device = PFC8591.PFC8591(debug)
					elif sensor['model'] == "BMP085":
						device = BMP085.BMP085(debug)
                                        elif sensor['model'] == "DS18B20":
                                                device = DS18B20.DS18B20(debug)
                                        elif sensor['model'] == "GPIOSTATUS":
                                                device = GPIOSTATUS.GPIOSTATUS(debug)
					elif sensor['model'] == "CPUTEMP":
                                                device = CPUTEMP.CPUTEMP(debug)
					else:
						device = 0

					if(device):
						if( device.SetOptions(sensor['options']) ):
							value = device.ReadValue()
							if(value is not False):
								if( Monitoring.SaveValueIsDifferent(sensor['id'], value, sensor['delta'], debug) is False):
									print "%s [ERROR]Błąd zapisu wartości do bazy" % datetime.now()
								else:
									if(debug):
										 print "%s [DEBUG]Zapis wartosci do bazy udany" % datetime.now()
							else:
								print "%s [ERROR]Błąd odczytu wartości z czujnika %s" % (datetime.now(), sensor['name'])
						else:
							print "%s [ERROR]Dla czujnika %s nie podano opcji lub podano błędne, lub czujnik nie działa" % (datetime.now(), sensor['name'])
					else:
						print "%s [WARNING]Typ czujnika nie obsługiwany" % datetime.now()
			else:	
				print "%s [WARNING]Brak sensorów" % datetime.now()
			#wylaczenie LM393
			GPIO.output(GPIO_LM393, DISABLE)
			time.sleep(Sleep_time)

			Monitoring.CloseDB()
		else:
			print "%s [ERROR]Błąd połączenia z bazą" % datetime.now()
