import json, urllib3

http = urllib3.PoolManager()
try:
    r = http.request('GET', 'http://ip.taobao.com/service/getIpInfo.php?ip=myip')
    ipInfo = json.loads(r.data.decode('utf-8'))
    ip = ipInfo['data']['ip']
    r = http.request('GET', 'https://www.tianqiapi.com/api/?appid=61544195&appsecret=XwU9hm4F&version=v6&ip='+ip)
    weater = json.loads(r.data.decode('utf-8'))

    print(weater)
except:
    pass
