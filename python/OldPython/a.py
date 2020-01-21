#-*- coding:utf-8 -*-

import sys
import getopt
import socket
import json
import time

def main():
    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # host = socket.gethostname() 
    host = '127.0.0.1'
    port = 16868
    print(ser)
    try:
        ser.connect((host, port))

    except:
        print('err')

    a = 'c3'
    ser.sendall(a.encode('utf-8'))

    ser.close()


    # # json_string = json.dumps(data)
    # # msg = ser.send(json_string.encode("utf-8"))
    # # json_string = json.dumps(data)
    # msg = ser.send(data.encode("utf-8"))
    # msg = ser.recv(1024)
    # # ser.close()
    # print (msg.decode('utf-8'))
    time.sleep(5)

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #声明socket类型，同时生成链接对象
    client.connect(('localhost',16868)) #建立一个链接，连接到本地的6969端口
    while True:
        # addr = client.accept()
        # print '连接地址：', addr
        msg = 'getAllSensorData'  #strip默认取出字符串的头尾空格
        client.send(msg.encode('utf-8'))  #发送一条信息 python3 只接收btye流
        data = client.recv(1024) #接收一个信息，并指定接收的大小 为1024字节
        print('recv:',data.decode('utf-8')) #输出我接收的信息
        time.sleep(1)
    client.close() #关闭这个链接
    