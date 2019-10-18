#-*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time,os
import control
import sys
from pathlib import Path
from multiprocessing import Process, Manager, Event

#定义默认配置
defaultGlobalConfig = {
    'GPIO' : {
        'ledWhitePin' : 16,
        'ledYellowPin' : 20,
        'ledRedPin' : 21,
        'lightSensorPin' : 26,
        'fireSensorPin' : 19,
        'pirSensorPin' : 17,
        'pirSensorEPin' : 23,
        'buzPin' : 12
    },
    'Hat' : {
        'devName' : '/dev/ttyUSB0',
        'sendSerPort' : '16868'
    }
}

#设定针脚编码模式为BCM
GPIO.setmode(GPIO.BCM)

#定义默认配置目录
CommonConfigDir = './config/'
configNameList = ['GPIO', 'Hat']

configManager = Manager().dict()

sensorDataList = Manager().dict()
hatEvent = Event()

# def loadConfig(globalGPIOConfig, globalHatConfig):
#     flag = 0
#     configPath = Path(defaultConfigPath)
#     if configPath.is_file():
#         print("找到配置文件")
#         flag = 1
#     else:
#         print("配置文件不存在，即将检查config目录是否存在")
#         with Path("./config") as dir:
#             if dir.is_dir():
#                 print("config目录存在")
#             else:
#                 print("config目录不存在，创建目录")
#                 try:
#                     dir.mkdir()
#                 except:
#                     print("创建config目录失败")
#                     return False
#         print("写入默认配置")
#         try:
#             if control.writeJson(defaultConfigPath,defaultConfigData):
#                 print("创建配置文件成功")
#                 flag = 1
#             else:
#                 print("创建配置文件失败,请删除config目录后重新运行程序")
#         except:
#             print("创建配置文件失败")
#     if flag == 1:
#         print('准备好了')
#         readConfig = control.readJson(defaultConfigPath)
#         globalHatConfig['devName'] = readConfig['devName']
        

#         print(dict)
#         # print(readConfig)




# def  test(status):
#     status.wait()
#     while True:
#         print(sensorDataList['hcho'])
#         time.sleep(1)

def main():
    # GPIO.setup(gpio_light_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.setup(gpio_pir_sensor_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.add_event_detect(gpio_light_sensor, GPIO.BOTH, callback=a, bouncetime=200)
    # GPIO.add_event_detect(gpio_light_sensor, GPIO.BOTH, callback=a, bouncetime=200)
    # GPIO.add_event_callback()
    # GPIO.cleanup()
    # #检查循环
    if control.initConfig(defaultGlobalConfig , configNameList) & control.loadConfig(configManager ,configNameList):
        pass
    else:
        sys.exit(2)
    



    control.savaConfig(defaultGlobalConfig, configManager, configNameList)
    # 启动子进程
    # testProcess = Process(target = test, args = (hatEvent, ))


    dataGetProcess = Process(target = control.getSensorData, args = (sensorDataList, hatEvent, ))
    dataSendSerProcess = Process(target = control.creatDataSendServer, args = (sensorDataList, hatEvent, 16868,))
    dataGetProcess.start()
    dataSendSerProcess.start()

    # # testProcess.start()
    dataSendSerProcess.join()


if __name__ == "__main__":
        main()


    
    
