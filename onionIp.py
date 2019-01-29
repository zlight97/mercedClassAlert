import requests

def getOnionIPList():
    myIP = requests.get('https://api.ipify.org').text
    ipList = requests.get('https://check.torproject.org/cgi-bin/TorBulkExitList.py?ip='+myIP+'&port=').text.split('#')
    a = ipList[len(ipList)-1]
    f=open("ipList.txt",'w')
    f.write(a)
    f.close()
getOnionIPList()