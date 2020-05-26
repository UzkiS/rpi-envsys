import RPi.GPIO as GPIO
import threading
import logging as LOG
import ctl
import json
import traceback
import sys
import time
import sqlite3
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

class sensorWatcher(threading.Thread):
    def __init__(self, uid):
        threading.Thread.__init__(self)
        self._uid = uid
        self._name = 'NONE'
        self._sleepTime = 1
        self._lastStatus = 0
        self._lastArarmTime1 = 0
        self._lastArarmTime2 = 0
        self._lastArarmTime3 = 0
        self._lastArarmTime4 = 0
        self._errCount = 0
        self._name, self._cname, self.unit, self._lowVar, self._highVar, self._mtd, self._alarmMode, self._useWatcher, self._useEmail, self._useBuz, self._recVal = self._getlVar()
        self._conn.close()
        self._GPIO = int(ctl.getGlobalVar('config')['CTL_GPIO'][self._name])
        pass

    def _getlVar(self):
        # ctl.getGlobalVar('sensorData')['temperature']
        self._conn = sqlite3.connect(sys.path[0] + '/' + ctl.getGlobalVar('config')['Common']['DB']).cursor()
        self._conn.execute("SELECT name, cname, unit, lowVar, highVar, method, alarmMode, useWatcher, useEmail, useBuz, recVal from sensor WHERE uid = ?", str(self._uid))
        for row in self._conn:
            return row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]
    
    def _getSafeVar(self):
        if self._mtd == 0:
            s = str(self._lowVar) + self.unit + ' 到 ' + str(self._highVar) + self.unit + ' 之间'   
        elif self._mtd == 1:
            s = '小于 ' + str(self._highVar) + self.unit
        return s

    # def _alarm(self):
    #     if self._lastStatus != self._status:
    #         if self._status == -1:
    #             if self._lastStatus == -1:
    #                 self._errCount = self._errCount + 1
    #             else:
    #                 self._errCount = 0
    #             if self._errCount >= 5:
    #                 print('status:' + self._name + " is error or not installed")
    #                 self._topic = '出错'
    #                 self._topicStatus = '传感器出错或未安装，请检查'
    #                 if self._lastArarmTime1 == 0:
    #                     self._sendEmail()
    #                     self._lastArarmTime1 = time.time()
    #                 elif time.time() - self._lastArarmTime1 < int(ctl.getGlobalVar('config')['Common']['alarmInterval']):
    #                     self._lastArarmTime1 = time.time()
    #                 else:
    #                     self._sendEmail()
    #                     self._lastArarmTime1 = time.time()
    #         elif self._status == 0:
    #             if self._lastStatus == -1 or self._lastStatus == 0:
    #                 pass
    #             else:
    #                 print('status:' + self._name + " is safe")
    #                 self._topic = '恢复安全'
    #                 self._topicStatus = '已经恢复安全状态'
    #                 if self._lastArarmTime2 == 0:
    #                     self._sendEmail()
    #                     self._lastArarmTime2 = time.time()
    #                 elif time.time() - self._lastArarmTime2 < int(ctl.getGlobalVar('config')['Common']['alarmInterval']):
    #                     self._lastArarmTime2 = time.time()
    #                 else:
    #                     self._sendEmail()
    #                     self._lastArarmTime2 = time.time()
    #         elif self._status == 1:
    #             print('status:' + self._name + " is danger")
    #             self._topic = '预警'
    #             self._topicStatus = '达到警戒值，请注意'
    #             if self._lastArarmTime3 == 0:
    #                 self._sendEmail()
    #                 self._lastArarmTime3 = time.time()
    #             elif time.time() - self._lastArarmTime3 < int(ctl.getGlobalVar('config')['Common']['alarmInterval']):
    #                 self._lastArarmTime3 = time.time()
    #             else:
    #                 self._sendEmail()
    #                 self._lastArarmTime3 = time.time()
    #         elif self._status == 2:
    #             print('status:' + self._name + " is warning")
    #             self._topic = '警告'
    #             self._topicStatus = '超过安全范围'
    #             if self._lastArarmTime4 == 0:
    #                 self._sendEmail()
    #                 self._lastArarmTime4 = time.time()
    #             elif time.time() - self._lastArarmTime4 < int(ctl.getGlobalVar('config')['Common']['alarmInterval']):
    #                 self._lastArarmTime4 = time.time()
    #             else:
    #                 self._sendEmail()
    #                 self._lastArarmTime4 = time.time()
    #         if self._lastStatus == -1 and self._errCount >= 5:
    #             pass
    #         else:
    #             self._lastStatus = self._status
    #         # status
    #         ### -1:err 0:safe 1:edge safe(yellow)  2.mail warning 3:buz warning(red)

    def _alarm(self):
        if self._lastStatus == self._status:
            if self._status == -1:
                self._errCount = self._errCount + 1
                # print('status:' + self._name + " error " + str(self._errCount))
                if self._errCount >= 10:
                    print('status:' + self._name + " is error or not installed")
                    self._topic = '出错'
                    self._topicStatus = '传感器出错或未安装，请检查'
                    self._GPIO_CTL()
                    if self._lastArarmTime1 == 0:
                        # self._sendEmail()
                        self._lastArarmTime1 = time.time()
                    elif time.time() - self._lastArarmTime1 < int(ctl.getGlobalVar('config')['Common']['alarmInterval']):
                        self._lastArarmTime1 = time.time()
                    else:
                        # self._sendEmail()
                        self._lastArarmTime1 = time.time()
        elif self._lastStatus != self._status:
            self._errCount = 0
            if self._status == -1:
                self._lastStatus = self._status
            elif self._status == 0:
                if self._lastStatus == -1:
                    pass
                else:
                    if self._mtd == 0:
                        if self.nowVar >= self._lowVar + self._recVal or self.nowVar <= self._highVar - self._recVal:
                            print('status:' + self._name + " is safe")
                            self._topic = '恢复安全'
                            self._topicStatus = '已经恢复安全状态'
                            self._GPIO_CTL()
                            if self._lastArarmTime2 == 0:
                                self._sendEmail()
                                self._lastArarmTime2 = time.time()
                            elif time.time() - self._lastArarmTime2 < int(ctl.getGlobalVar('config')['Common']['alarmInterval']):
                                self._lastArarmTime2 = time.time()
                            else:
                                self._sendEmail()
                                self._lastArarmTime2 = time.time()
                            self._lastStatus = self._status
                        else:
                            self._lastArarmTime4 = time.time()
                    if self._mtd == 1:
                        if self._lastStatus == 1 or self._lastStatus == 2:
                            if self.nowVar <= self._lowVar - self._recVal:
                                print('status:' + self._name + " is safe")
                                self._topic = '恢复安全'
                                self._topicStatus = '已经恢复安全状态'
                                self._GPIO_CTL()
                                if self._lastArarmTime2 == 0:
                                    self._sendEmail()
                                    self._lastArarmTime2 = time.time()
                                elif time.time() - self._lastArarmTime2 < int(ctl.getGlobalVar('config')['Common']['alarmInterval']):
                                    self._lastArarmTime2 = time.time()
                                else:
                                    self._sendEmail()
                                    self._lastArarmTime2 = time.time()
                                self._lastStatus = self._status
                        else:
                            if self._lastStatus == 1:
                                self._lastArarmTime3 = time.time()
                            elif self._lastStatus == 2:
                                self._lastArarmTime4 = time.time()
                        # if self._lastStatus == 2:
                        #     if self.nowVar <= self._highVar - self._recVal:
                        #         print('status:' + self._name + " is safe")
                        #         self._topic = '恢复安全'
                        #         self._topicStatus = '已经恢复安全状态'
                        #         if self._lastArarmTime2 == 0:
                        #             self._sendEmail()
                        #             self._lastArarmTime2 = time.time()
                        #         elif time.time() - self._lastArarmTime2 < int(ctl.getGlobalVar('config')['Common']['alarmInterval']):
                        #             self._lastArarmTime2 = time.time()
                        #         else:
                        #             self._sendEmail()
                        #             self._lastArarmTime2 = time.time()
                        #         self._lastStatus = self._status
                        #     else:
                        #         self._lastArarmTime4 = time.time()
            elif self._status == 1:
                if self._lastStatus == -1 or self._lastStatus == 0:
                    print('status:' + self._name + " is warning")
                    self._topic = '预警'
                    self._topicStatus = '达到警戒值，请注意'
                    self._GPIO_CTL()
                    if self._lastArarmTime3 == 0:
                        self._sendEmail()
                        self._lastArarmTime3 = time.time()
                    elif time.time() - self._lastArarmTime3 < int(ctl.getGlobalVar('config')['Common']['alarmInterval']):
                        self._lastArarmTime3 = time.time()
                    else:
                        self._sendEmail()
                        self._lastArarmTime3 = time.time()
                else:
                    if self.nowVar <= self._highVar - self._recVal:
                        print('status:' + self._name + " is warning")
                        self._topic = '恢复预警状态'
                        self._topicStatus = '恢复到预警范围，请注意'
                        self._GPIO_CTL()
                        if self._lastArarmTime3 == 0:
                            self._sendEmail()
                            self._lastArarmTime3 = time.time()
                        elif time.time() - self._lastArarmTime3 < int(ctl.getGlobalVar('config')['Common']['alarmInterval']):
                            self._lastArarmTime3 = time.time()
                        else:
                            self._sendEmail()
                            self._lastArarmTime3 = time.time()
                    self._lastStatus = self._status
            elif self._status == 2:
                print('status:' + self._name + " is danger")
                self._topic = '警告'
                self._topicStatus = '超过安全范围'
                self._GPIO_CTL()
                if self._lastArarmTime4 == 0:
                    self._sendEmail()
                    self._lastArarmTime4 = time.time()
                elif time.time() - self._lastArarmTime4 < int(ctl.getGlobalVar('config')['Common']['alarmInterval']):
                    self._lastArarmTime4 = time.time()
                else:
                    self._sendEmail()
                    self._lastArarmTime4 = time.time()
                self._lastStatus = self._status

    def _GPIO_CTL(self):
        if self._GPIO != -1:
            if self._status == -1 and self._errCount >= 5:
                GPIO.output(self._GPIO, GPIO.LOW)
                print(self._cname + " set GPIO.LOW")
            elif self._status == 0:
                GPIO.output(self._GPIO, GPIO.LOW)
                print(self._cname + " set GPIO.LOW")
            elif self._status == 1:
                GPIO.output(self._GPIO, GPIO.HIGH)
                print(self._cname + " set GPIO.HIGH")
            elif self._status == 2:
                GPIO.output(self._GPIO, GPIO.HIGH)
                print(self._cname + " set GPIO.HIGH")

    def _sendEmail(self):
        if self._useEmail == 1:
            def _format_addr(s):
                name, addr = parseaddr(s)
                return formataddr((Header(name, 'utf-8').encode(), addr))
            fromAddr = ctl.getGlobalVar('config')['Mail']['smtpUser']
            smtpPassword = ctl.getGlobalVar('config')['Mail']['smtpPassword']
            smtpServer = ctl.getGlobalVar('config')['Mail']['smtpServer']
            smtpPort = ctl.getGlobalVar('config')['Mail']['smtpPort']
            toAddr = ctl.getGlobalVar('config')['Mail']['mailReceiver']

            msgHtml = '<html><body><h1>' + self._cname + self._topic + '</h1>' + '<p>' + self._cname + self._topicStatus + '。</p>' + '<p>当前值为 ' + str(self.nowVar) + self.unit + ' ,安全值为 ' + str(self._getSafeVar()) + '。</p>' + '</body></html>'
            msgTopic = self._cname + self._topic + ' ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            msg = MIMEText(msgHtml, 'html', 'utf-8')
            # msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
            msg['From'] = _format_addr('Raspberry Pi <%s>' % fromAddr)
            msg['To'] = _format_addr(toAddr + ' <%s>' % toAddr)
            msg['Subject'] = Header(msgTopic, 'utf-8').encode()
            
            try:
                server = smtplib.SMTP(smtpServer, smtpPort)
                # server.set_debuglevel(1)
                server.login(fromAddr, smtpPassword)
                server.sendmail(fromAddr, [toAddr], msg.as_string())
                print(self._name + ' sendEmail')
                server.quit()
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_traceback))
                LOG.error(traceback.format_exception(exc_type, exc_value, exc_traceback))
            else:
                LOG.info(self._name + 'send email success')

    def _startBuz(self):
        pass

    def _watchVar(self):
        #method: 
        ### 0 : low < data > high red alar
        ### 1 : data > low > high
        ### 1 : data > low > high
        # alarmMode:
        ### 0:NORMAL
        ### 1:BUZ
        #'flag' + name.capitalize():-1 gray 0:green 1:yellow 2:red
        self._name, self._cname, self.unit, self._lowVar, self._highVar, self._mtd, self._alarmMode, self._useWatcher, self._useEmail, self._useBuz, self._recVal = self._getlVar()
        self._conn.close()
        self._msg = 'Sensor [' + self._name + '] watch thread started.'
        LOG.info(self._msg)
        print(self._msg)
        while True:
            if ctl.getGlobalVar('sensorData') != False:
                self.nowVar = ctl.getGlobalVar('sensorData')[self._name]
                # print(self.nowVar)
                # time.sleep(sleepTime)
                # ctl.setGlobalVar('flag' + name.capitalize() , 1)
                ### 0 : low < data > high
                ### 1 : data < low < high
                if self._mtd == 0 :
                    if 0 < self.nowVar < self._lowVar:
                        self._status = 2
                    elif self.nowVar > self._highVar:
                        self._status = 2
                    elif self.nowVar == -1:
                        self._status = -1
                    else:
                        self._status = 0
                elif self._mtd == 1:
                    if self.nowVar >= self._highVar:
                        self._status = 2
                    elif self.nowVar >= self._lowVar:
                        self._status = 1
                    elif self.nowVar == -1:
                        self._status = -1
                    else:
                        self._status = 0
                # self._conn = sqlite3.connect(sys.path[0] + '/' + ctl.getGlobalVar('config')['Common']['DB']).cursor()
                # self._conn.execute("SELECT useEmail, useBuz from sensor WHERE uid = ?", str(self._uid))
                # for row in self._conn:
                #     print(row[0], row[1])
                ctl.setFlagVar(self._name, self._status)
                # print(self._cname + str(self._status))
                self._alarm()
                time.sleep(1)
                

    
    def run(self):
        # conn = sqlite3.connect(sys.path[0] + '/' + ctl.getGlobalVar('config')['Common']['DB']).cursor()
        # self._name, self._lowVar, self._highVar, self._mtd, self._alarmMode, self._useEmail, self._useBuz = self._getlVar(conn)
        # print(name, lowVar, highVar, mtd)
        if self._useWatcher == 1:
            self._watchVar()
        else:
            ctl.setFlagVar(self._name, -2)
        # while