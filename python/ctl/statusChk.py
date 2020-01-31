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
        self._name = 'NONE'
        self._sleepTime = 1
        conn = sqlite3.connect(sys.path[0] + '/' + ctl.getGlobalVar('config')['Common']['DB']).cursor()
        self._name, self._lowVar, self._highVar, self._mtd, self._alarmMode, self._useEmail, self._useBuz = self.getlVar(conn)
        pass

    def getlVar(self, cursor):
        # ctl.getGlobalVar('sensorData')['temperature']
        cursor.execute("SELECT name, lowVar, highVar, method, alarmMode, useEmail, useBuz from sensor WHERE uid = ?", str(self._uid))
        for row in cursor:
            return row[0], row[1], row[2], row[3], row[4], row[5], row[6]

    def alarm(self):
        if self._status == -1:
            print('status:' + self._name + " is not installed")
        elif self._status == 0:
            print('status:' + self._name + " is safe")
        elif self._status == 1:
            print('status:' + self._name + " is danger")
        elif self._status == 2:
            print('status:' + self._name + " is warning")
        # status
        ### -1:err 0:safe 1:edge safe(yellow)  2.mail warning 3:buz warning(red)
        pass

    def watchVar(self):
        #method: 
        ### 0 : low < data > high red alar
        ### 1 : data > low > high
        ### 1 : data > low > high
        # alarmMode:
        ### 0:NORMAL
        ### 1:BUZ
        #'flag' + name.capitalize():-1 gray 0:green 1:yellow 2:red
        self._msg = 'Sensor [' + self._name + '] watch thread started.'
        LOG.info(self._msg)
        print(self._msg)
        while True:
            if ctl.getGlobalVar('sensorData') != False:
                nowVar = ctl.getGlobalVar('sensorData')[self._name]
                # print(nowVar)
                # time.sleep(sleepTime)
                # ctl.setGlobalVar('flag' + name.capitalize() , 1)
                ### 1 : low < data > high
                if mtd == 0 :
                    if 0 < nowVar < lowVar:
                        self._status = 3
                    elif nowVar > highVar:
                        self._status = 3
                    elif nowVar == -1:
                        self._status = -1
                    else:
                        self._status = 0
                elif mtd == 1:
                    if nowVar >= highVar:
                        self._status = 2
                    elif nowVar >= lowVar:
                        self._status = 1
                    elif nowVar == -1:
                        self._status = -1
                    else:
                        self._status = 0
                ctl.setFlagVar(self._name, status)
                self.alarm()
                

    
    def run(self):
        # conn = sqlite3.connect(sys.path[0] + '/' + ctl.getGlobalVar('config')['Common']['DB']).cursor()
        # self._name, self._lowVar, self._highVar, self._mtd, self._alarmMode, self._useEmail, self._useBuz = self.getlVar(conn)
        # print(name, lowVar, highVar, mtd)
        self.watchVar(self._name)
        # while