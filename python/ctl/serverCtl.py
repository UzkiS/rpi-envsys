import time,os
import sys
import socket
import threading
import logging as LOG
import traceback
import ctl
import json

##### 前后端数据传输线程
class pushSensorData(threading.Thread):
    def __init__(self, host = '127.0.0.1', port = 16868):
        threading.Thread.__init__(self)
        self._port = port
        self._host = host
        self._flag = True
        pass

    def creatPushServer(self):
        time.sleep(3)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while self._flag:
            try:
                server.bind((self._host, self._port))
            except:
                self._msg = 'Push data thread failed to start, retry ...'
                print(self._msg)
                LOG.warning(self._msg)
                time.sleep(3)
            else:
                self._msg = 'Push data thread started. Port [' + str(self._port) + '] Host [' + self._host + ']'
                LOG.info(self._msg)
                print(self._msg)
                self._flag = False
        server.listen(5)
        # server.settimeout(5)
        conn_list = []
        coon_sock = {}
        self._flag = True
        while self._flag:
            conn, addr = server.accept()
            self._msg = 'Client connectd' + str(addr)
            if addr not in conn_list:
                conn_list.append(addr)
                coon_sock[addr] = conn
            threading.Thread(target=self.tcpLink, args=(conn, addr)).start()

    def tcpLink(self, conn, addr):
        print(self._msg)
        LOG.info(self._msg)
        cont = 0
        while self._flag:
            try:
                data = conn.recv(1024).decode('utf-8')
                if data != None or data != '' or data != ' ' or data != False:
                    pass
                    # print(data)
                    # time.sleep(1)
                if data == 'getAllSensorData':
                    # if ctl.getGlobalVar('sensorData'):
                    #     conn.send(json.dumps(ctl.getGlobalVar('sensorData')).encode('utf-8'))
                    print('recive:' + data)
                    conn.send(json.dumps(ctl.getGlobalVar('sensorData')).encode('utf-8'))
                    conn.close()
                    break
                    # print(ctl.getGlobalVar('sensorData').encode('utf-8'))
                elif data == 'getAllSensorDataWithStatus':
                    # if ctl.getGlobalVar('sensorData'):
                    #     conn.send(json.dumps(ctl.getGlobalVar('sensorData')).encode('utf-8'))
                    print('recive:' + data)
                    sensorData = ctl.getGlobalVar('sensorData')
                    sensorDataStatus = ctl.getGlobalVar('flag')
                    # sensorDataStatus = ctl.getGlobalVar('sensorDataStatus')
                    result = {}
                    for item in sensorData:
                        result[item] = {}
                        result[item]['data'] = sensorData[item]
                        result[item]['status'] = sensorDataStatus[item]
                    conn.send(json.dumps(result).encode('utf-8'))
                    conn.close()
                    break
                    # print(ctl.getGlobalVar('sensorData').encode('utf-8'))
                else:
                    cont = cont + 1
                    if cont >= 5:
                        raise Exception('Client maybe closed')
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_traceback))
                LOG.error(traceback.format_exception(exc_type, exc_value, exc_traceback))
                break
            
    def run(self):
        while not ctl.getGlobalVar('flagPushD'):
            pass
        self.creatPushServer()