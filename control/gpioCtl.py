#-*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

def setBuz(channel, time = 1):
    GPIO.output(channel, GPIO.HIGH)
    time.sleep(time)
    GPIO.output(channel, GPIO.LOW)