#-*- coding:utf-8 -*-

import sys
import getopt
import socket
import json

def main():
    cmd_params = sys.argv[1:]
    if sys.argv[1:] == []:
        print ('usage:python3 getSensorData.py -i <sensorID> -u ')
        sys.exit(2)
    unit = 0
    # print(cmd_params)
    try:
        opts, args = getopt.gnu_getopt(cmd_params, 'hi:u',['id=', 'unit'])
    except:
         print ('usage:python3 getSensorData.py -i <sensorID> -u ')
         sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('usage:python3 getSensorData.py -i <sensorID> -u ')
        elif opt in ("-i", "--id"):
            sensorID = arg
        elif opt == '-u':
            try:
                sensorID
            except NameError:
                print ('usage:python3 getSensorData.py -i <sensorID> -u ')
                sys.exit(2)
            else:
                unit = 1

    

    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    host = socket.gethostname() 
    port = 16868
    ser.connect((host, port))
    data = [sensorID, unit]
    json_string = json.dumps(data)
    msg = ser.send(json_string.encode("utf-8"))
    msg = ser.recv(1024)
    ser.close()
    print (msg.decode('utf-8'))

if __name__ == "__main__":
    main()
    