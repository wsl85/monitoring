#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO
from datetime import datetime

ENABLE = 1
DISABLE = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_OUT1 = 26
GPIO_OUT2 = 19
GPIO_OUT3 = 13
GPIO_OUT4 = 6
GPIO_OUT5 = 23
GPIO_OUT6 = 24

GPIO.setup(GPIO_OUT1, GPIO.OUT)
GPIO.setup(GPIO_OUT2, GPIO.OUT)
GPIO.setup(GPIO_OUT3, GPIO.OUT)
GPIO.setup(GPIO_OUT4, GPIO.OUT)
GPIO.setup(GPIO_OUT5, GPIO.OUT)
GPIO.setup(GPIO_OUT6, GPIO.OUT)

GPIO.output(GPIO_OUT1,0)
GPIO.output(GPIO_OUT2,0)
GPIO.output(GPIO_OUT3,1)
GPIO.output(GPIO_OUT4,1)
GPIO.output(GPIO_OUT5,0)
GPIO.output(GPIO_OUT6,0)

