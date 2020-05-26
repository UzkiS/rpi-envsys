import RPi.GPIO as GPIO
import threading
import logging as LOG
import ctl
import traceback
import sys
import time

class lcd(threading.Thread):
    def __init__(self, channel, lcdChannel, upTime = 60):
        threading.Thread.__init__(self)
        self._channel=channel
        self._lcdChannel=lcdChannel
        self._timeLimit=upTime
        self._upTime=upTime
        self._lastStatus=1
        pass

    def lcdTimer(self):
        while 1:
            if GPIO.input(self._channel)==1:
                self._upTime=self._timeLimit
                # print(self._upTime)
            else:
                self._upTime=self._upTime-1
                
            if self._upTime==0:
                GPIO.output(self._lcdChannel, GPIO.LOW)
                if self._lastStatus == 1:
                    print(self._upTime)
                    print('close LCD')
                    self._lastStatus = 0
            elif self._upTime==60:
                GPIO.output(self._lcdChannel, GPIO.HIGH)
                if self._lastStatus == 0:
                    print('open LCD')
                    self._lastStatus = 1
            time.sleep(1)
        



        
    def run(self):
        self.lcdTimer()