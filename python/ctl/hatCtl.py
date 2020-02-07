import threading
import logging as LOG
import serial
import ctl
import json
import traceback
import sys
import time

    
##### 获取数据线程
class pullHatData(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        pass
    def pullData(self, dev = '/dev/ttyAMA0', baudRate = 9600):

        while True:
            # ctl.setGlobalVar('sensorData', '')
            self._msg = 'Pull data thread started.'
            print(self._msg)
            # ctl.setGlobalVar('flagPushD', True)
            self._errCount=0
            try:
                serialFd = serial.Serial(dev , baudRate, timeout=0)
                self._msg = 'Hat insert.'
                LOG.info(self._msg)
            except:
                time.sleep(1)
                print('Watting hat insert...')
                continue
            try:
                while True:
                    waitSize = serialFd.in_waiting
                    if waitSize != 0:
                        time.sleep(1)
                        self._errCount = 0
                        buf = serialFd.readline()
                        # print(buf)
                        readData = buf.decode('utf-8')
                        sensorData = json.loads(readData)
                        ctl.setGlobalVar('sensorData', sensorData)
                        # print(readData)
                        
                        ctl.setGlobalVar('flagPushD', True)
                    #     ctl.setGlobalVar('flagPushD', True)
                    else:
                        self._errCount = self._errCount + 1
                        time.sleep(1)
                        if self._errCount > 10:
                            raise Exception("Read hat data error, may be hat pull out.")

            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_traceback))
                LOG.error(traceback.format_exception(exc_type, exc_value, exc_traceback))
                print('Hat error or disconnected.')
                time.sleep(2)
                serialFd.close()
                continue
        



        
    def run(self):
        self.pullData(ctl.getGlobalVar('config')['Hat']['serialDeviceName'], ctl.getGlobalVar('config')['Hat']['baudRate'])