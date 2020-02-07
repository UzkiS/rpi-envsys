import threading
import logging as LOG
import serial
import ctl
import json
import traceback
import sys
import time

while True:
    # ctl.setGlobalVar('sensorData', '')
    msg = 'Pull data thread started.'
    # LOG.info(self._msg)
    print(msg)
    # ctl.setGlobalVar('flagPushD', True)
    try:
        serialFd = serial.Serial('/dev/ttyS4' , 9600, timeout=0)
        print('2')
    except:
        time.sleep(1)
        continue
    try:
        while True:
            buf = '1'
            waitSize = serialFd.in_waiting
            if waitSize != 0:
                time.sleep(1)
                buf = serialFd.readline()
                # print(buf)
                readData = buf.decode('utf-8')
                # print(readData)
                print('1')
                sensorData = json.loads(readData)
                # ctl.setGlobalVar('sensorData', sensorData)
                print(readData)
                
                # ctl.setGlobalVar('flagPushD', True)
            #     ctl.setGlobalVar('flagPushD', True)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_traceback))
        # LOG.error(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print('Hat error or disconnected')
        time.sleep(2)
        serialFd.close()
        continue