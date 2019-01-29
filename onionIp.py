import requests

def getOnionIPList():
    try:
        print "getting ip list"
        myIP = requests.get('https://api.ipify.org').text
        ipList = requests.get('https://check.torproject.org/cgi-bin/TorBulkExitList.py?ip='+myIP+'&port=').text.split('#')
        a = ipList[len(ipList)-1]
        f=open("ipList.txt",'w')
        f.write(a)
        print "ip list written"
        f.close()
    except:
        time.sleep(10)
        getOnionIPList()