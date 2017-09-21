#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO

ENABLE = 1
DISABLE = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_OUT3 = 22

OUT3_RUNNING = 30

GPIO.setup(GPIO_OUT3, GPIO.OUT)
GPIO.output(GPIO_OUT3, DISABLE)

def OutputRunning(gpio,time_running):
        GPIO.output(gpio,ENABLE)
        time.sleep(time_running)
        GPIO.output(gpio,DISABLE)
        return

if __name__ == "__main__":
	OutputRunning(GPIO_OUT3, OUT3_RUNNING)

