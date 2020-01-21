class globalVar:
    var = {
        'flag' : {
            'formaldehyde' : -1,
            'temperature' : -1, 
            'humditiy' : -1,
            'light' : -1
        }
    } 

def setGlobalVar(name, val):
    try:
        globalVar.var[name] = val
    except:
        return False
    else:
        return True

def setFlagVar(name, val):
    try:
        globalVar.var['flag'][name] = val
    except:
        return False
    else:
        return True

def getGlobalVar(name):
    if name in globalVar.var:
        return globalVar.var[name]
    else:
        return False

def getFlaglVar(name):
    if name in globalVar.var['flag']:
        return globalVar.var['flag'][name]
    else:
        return False

def removeGlobalVar(name):
    try:
        globalVar.var.pop(name)
    except:
        return False
    else:
        return True