#-*- coding:utf-8 -*-

import json
from pathlib import Path
from multiprocessing import Manager

#定义写json函数
def writeJson(pwd, data):
    try:
        with Path(pwd).open(mode ='w') as f:
            json.dump(data, f, ensure_ascii=False,indent=4)
        return True
    except:
        return False

def readJson(pwd):
    with Path(pwd).open(mode ='r') as f:
        data = json.load(f)
        return data

def initConfig(defaultGlobalConfig, configNameList, configDir = './config/'):
    flag = 0
    with Path('./config') as dir:
        if dir.is_dir():
            # print('Config directory exists.')
            pass
        else:
            print('Config directory doesn\'t exist, try to create it.')
            try:
                dir.mkdir()
            except:
                print('Config directory creation failed.')
            else:
                print('Config directory created successfully.')
                flag = 1
    for configName in configNameList:
        configFilePath = configDir + configName + '.json'
        configFileData = defaultGlobalConfig[configName]
        configFile = Path(configFilePath)
        if configFile.is_file():
            print('Found config : ' + configFilePath)
            flag = 1
        else:
            print('Can\'t find config : ' + configFilePath + ', create it.')
            try:
                if writeJson(configFilePath,configFileData):
                    print('Create ' + configName + '.json success')
                    flag = 1
                else:
                    print('Failed to create ' + configName + ' config file')
                    flag = 0
            except:
                print('Failed to create file')
                flag = 0
    if flag == 1:
        print('Config files check success')
        print(' ')
        return True
    else:
        print('Config files check failed')
        print(' ')
        return False



def savaConfig(defaultGlobalConfig, configManager, configNameList, configDir = './config/'):
    for configName in configNameList:
        dict = {}
        configFilePath = configDir + configName + '.json'
        try:
            for key in configManager.keys():
                if key in defaultGlobalConfig[configName]:
                    dict[key] = configManager[key]
                writeJson(configFilePath, dict)
        except:
            print('Save config error.')
        finally:
            dict.clear()




def loadConfig(configManager, configNameList, configDir = './config/'):
    flag = 0
    for configName in configNameList:
        configFilePath = configDir + configName + '.json'
        try:
            LoadedConfigData = readJson(configFilePath)
            # print(LoadedConfigData)
            for key in LoadedConfigData.keys():
                configManager[key] = LoadedConfigData[key]                
        except:
            print('Load ' + configName + '.json failed')
            return False
        else:
            print('Load ' + configName + '.json success')
            flag = 1
    print(' ')
    if flag == 1:
        return True