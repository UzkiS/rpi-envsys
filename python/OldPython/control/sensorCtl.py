#-*- coding:utf-8 -*-

import serial
import time
import numpy
import socket
import json
import sys
import copy

errTips = 'Data Error'

class sensor:
    def __init__(self, name , hightNum, lowNum, unit, onlyLow = 0):
        self.name = name
        self.hightNum = hightNum
        self.lowNum = lowNum
        self.unit = unit
        self.onlyLow = onlyLow

    def checkData(self):
        if self.onlyLow == 0:
            if self.hightNum == 238 & self.lowNum == 238:
                return False
            else:
                return True
        else:
            if self.lowNum == 238:
                return False
            else:
                return True

    def getData(self):
        if self.checkData():
            result = self.hightNum * 256 + self.lowNum
        else:
            result = errTips
        return result
    
    def getUnit(self):
        if self.checkData():
            result = self.unit
        else:
            result = ''
        return result
    
    # def getDataWithUnit(self):
    #     if self.checkData():
    #         # return str(self.getData()) + " " + self.unit
    #         return self.getData(), self.unit
    #     else:
    #         return str(self.getData())

def creatDataSendServer(dict, event, port = 16868, host = '127.0.0.1'):
    event.wait()
    sensorList = ['hcho', 'temp', 'humi', 'tvoc', 'eco2']
    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = host
    port = port
    try:
        ser.bind((host, port))
    except:
        print('SendSer start error, the port may be occupied')
        sys.exit(2)
        return False

    print("SendSer started on port ", port, ", listen on ", host)
    ser.listen(5)
    while True: 
        try:
            clientSocket,addr = ser.accept()
        except:
            return False
        print("addr: %s" % str(addr))
        # data = clientSocket.recv(1024)
        # try:
        #     data = json.loads(data.decode('utf-8'))
        #     sensorListIndex=data[0]
        #     dictIndex=sensorList[int(sensorListIndex)]
        #     if data[1] == 1:
        #         unitDictIndex = dictIndex + 'Unit'
        #         waitSendData = str(dict[dictIndex]) + ' ' + dict[unitDictIndex]
        #     else:
        #         waitSendData = dict[dictIndex]
        # except:
        #     waitSendData = 'Error'
        # waitSendData=json.dumps(list())
        nowDict=copy.deepcopy(dict)
        # print(json.dumps(nowDict))
        msg=json.dumps(nowDict)
        print(nowDict)
        print(dict)

        # # msg = str(waitSendData)
        # msg=waitSendData
        # # msg = 'welcome' + "\r\n"
        clientSocket.send(msg.encode('utf-8'))
        clientSocket.close()


def getSensorData(dict, event, dev = '/dev/ttyS0'):
    with serial.Serial(dev , 9600, timeout=0) as ser:
        try:
            while True:
                size = ser.in_waiting           # 获得缓冲区字符
                while size != 12:
                    # print(size)
                    time.sleep(1)
                    size = ser.in_waiting
                    continue
                if size != 0:
                    checkSum = 0
                    response = ser.read(size)       # 读取内容并显示
                    for i in range(1,size - 1):
                        checkSum += response[i]
                        print(response)
                    if hex(~numpy.uint32(checkSum)+1)[8] + hex(~numpy.uint32(checkSum)+1)[9] != response.hex()[22] + response.hex()[23]:
                        pass
                    else:
                        hchoHightNum = response[1]
                        hchoLowNum = response[2]
                        dhtTempLowNum = response[3]
                        dhtHumiLowNum = response[4]
                        tvocHightNum = response[5]
                        tvocLowNum = response[6]
                        eco2HightNum = response[7]
                        eco2LowNum = response[8]
                        hcho = sensor('HCHO', hchoHightNum, hchoLowNum, 'PPb')
                        temp = sensor('Temperature', 0, dhtTempLowNum, '℃', 1)
                        humi = sensor('Humidity', 0, dhtHumiLowNum, '%', 1)
                        tvoc = sensor('TVOC', tvocHightNum, tvocLowNum, 'PPb')
                        eco2 = sensor('eCO2', eco2HightNum, eco2LowNum, 'PPm')
                        try:
                            dict['hcho'] = hcho.getData()
                            dict['hchoUnit'] = hcho.getUnit()
                            dict['temp'] = temp.getData()
                            dict['tempUnit'] = temp.getUnit()
                            dict['humi'] = humi.getData()
                            dict['humiUnit'] = humi.getUnit()
                            dict['tvoc'] = tvoc.getData()
                            dict['tvocUnit'] = tvoc.getUnit()
                            dict['eco2'] = eco2.getData()
                            dict['eco2Unit'] = eco2.getUnit()
                        except:
                            # print('Set sensor data error')
                            # sys.exit(2)
                            # return False
                            pass

                        event.set()

                    ser.reset_input_buffer()                 # 清空接收缓存区
                    time.sleep(0.1)                  # 软件延时
        except KeyboardInterrupt:
            event.clear()
            ser.close()
