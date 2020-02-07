# import RPi.GPIO as GPIO
import time,os
import sys
import socket
from pathlib import Path
import threading
from configobj import ConfigObj
import logging as LOG
import traceback
import ctl
import subprocess
## 预定义变量
configPath = sys.path[0]+'/config.conf'
logPath = sys.path[0]+'/logs/envsys.log'
## 预定义全局线程锁
ctl.setGlobalVar('flagPushD', False)

## 预定义日志选项
LOG.basicConfig(filename=logPath, format='%(asctime)s    %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=LOG.DEBUG,)

## 定义线程
##### 保存配置线程
class saveConfig(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        pass
    def run(self):
        pass



##### 显示屏控制线程
class ctlLCD(threading.Thread):
    def __init__(self,pin):
        threading.Thread.__init__(self)
        self._pin = pin
        pass
    def run(self):
        print(config)
    
##主程序开始
###读取配置
# config = ConfigObj(configPath)
ctl.setGlobalVar('config', ConfigObj(configPath))
config=ctl.getGlobalVar('config')


# print(ctl.getGlobalVar('config'))
# config.write()
### 预设GPIO状态
# outputHighList = [config['GPIO']['LCD']]
# outputLowList = [config['GPIO']['BUZ']]
# inputList = [config['GPIO']['PIR'], config['GPIO']['LDR']]

# GPIO.setup(outputHighList, GPIO.OUT, initial=GPIO.HIGH)
# GPIO.setup(chanOutLowList, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(inputList, GPIO.IN)


# ThreadPullSD = pullSensorData()
# ThreadPSD.setDaemon(True)
# ThreadPSD.start()

# ThreadCL = ctlLCD(config['GPIO']['LCD'])
# ThreadCL.setDaemon(True)
# ThreadCL.start()

# ThreadCL.join()
if config['Common']['usePHPWebServer'] == 1:
    class phpProcess(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            pass
        def run(self):
            subprocess.run('php -S localhost:'+ config['Common']['httpPort'] +' -t ' + sys.path[0] + '/web/ &', shell=True)
            # subprocess.run('php -S localhost:'+ config['Common']['httpPort'] +' -t ' + sys.path[0] + '/web/ &> /tmp/sysenv_php.log', shell=True)
            # os.execl('/usr/bin/php','php','-S', 'localhost:'+ config['Common']['httpPort'], '-t', sys.path[0] + '/web/')
    ThreadPHP = phpProcess()
    ThreadPHP.setDaemon(True)
    ThreadPHP.start()


### 传感器数据获取线程
ThreadPullD = ctl.pullHatData()
ThreadPullD.setDaemon(True)
ThreadPullD.start()

time.sleep(3)

# ### 传感器数据推送线程
ThreadPushD = ctl.pushSensorData(config['Common']['host'], int(config['Common']['sendSerPort']))
ThreadPushD.setDaemon(True)
ThreadPushD.start()

### 状态检测线程
# for i in range(1, 7):
ThreadStatusCheck = {}
for i in range(1, 7):
    ThreadStatusCheck[i] = ctl.sensorWatcher(i)
    ThreadStatusCheck[i].setDaemon(True)
    ThreadStatusCheck[i].start()

    # print(i)
# ThreadPullD = ctl.hatCtl.pullHatData()
# ThreadPullD.setDaemon(True)
# ThreadPullD.start()

# ThreadPullD.join()

time.sleep(5)
# print(ctl.getGlobalVar('flag'))

#绑定要监听的端口
# ThreadPullD.join()
ThreadPullD.join()

# try:
#     pass
# except:
#     if config['Common']['usePHPWebServer'] == 1:
#         subprocess.run('pkill -9 php', shell=True)