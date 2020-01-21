import threading
import logging as LOG
import ctl
import json
import traceback
import sys
import time
import sqlite3

class sensor(threading.Thread):
    def __init__(self, uid):
        threading.Thread.__init__(self)
        self._uid = uid
        pass

    def getlVar(self, cursor):
        # ctl.getGlobalVar('sensorData')['temperature']
        cursor.execute("SELECT name, lowVar, highVar, method, alarmMode from sensor WHERE uid = ?", str(self._uid))
        for row in cursor:
            return row[0], row[1], row[2], row[3], row[4]

    def alarm(self, status, alarmMode = 0):
        # status
        ### -1:err 0:safe 1:edge safe(yellow)  2.mail warning 3:buz warning(red)
        pass

    def watchVar(self, name, lowVar, highVar, mtd, alarmMode = 0,sleepTime = 1):
        #method: 
        ### 0 : low < data > high red alar
        ### 1 : data > low > high
        ### 1 : data > low > high
        # alarmMode:
        ### 0:NORMAL
        ### 1:BUZ
        #'flag' + name.capitalize():-1 gray 0:green 1:yellow 2:red
        self._msg = 'Sensor [' + name + '] watch thread started.'
        LOG.info(self._msg)
        print(self._msg)
        while True:
            if ctl.getGlobalVar('sensorData') != False:
                nowVar = ctl.getGlobalVar('sensorData')[name]
                # print(nowVar)
                # time.sleep(sleepTime)
                # ctl.setGlobalVar('flag' + name.capitalize() , 1)
                ### 1 : low < data > high
                if mtd == 0 :
                    if 0 < nowVar < lowVar:
                        status = 3
                    elif nowVar > highVar:
                        status = 3
                    elif nowVar == -1:
                        status = -1
                    else:
                        status = 0
                elif mtd == 1:
                    if nowVar >= highVar:
                        status = 2
                    elif nowVar >= lowVar:
                        status = 1
                    elif nowVar == -1:
                        status = -1
                    else:
                        status = 0
                ctl.setFlagVar(name, status)
                self.alarm(status)
                

    
    def run(self):
        conn = sqlite3.connect(ctl.getGlobalVar('config')['Common']['DB']).cursor()
        name, lowVar, highVar, mtd, alarmMode = self.getlVar(conn)
        # print(name, lowVar, highVar, mtd)
        self.watchVar(name, lowVar, highVar, mtd, alarmMode)
        # while