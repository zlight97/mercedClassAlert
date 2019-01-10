import json
import requests
import classAlert

def write(file, jData):
	with open(file, "w") as r:
		r.write(json.dumps(jData, sort_keys=True, indent=4, separators=(',', ':')))

def populateTerm():
    term = classAlert.checkTerm()
    htmlData = requests.get('https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.P_ViewSchedule?validterm='+term+'&subjcode=ALL&openclasses=N')
    arrayObj = {}
    arrayObj["list"] = []
    jsonObject = {}
    for text in htmlData.text.split("&crsenumb="):
        loc = text.split("=")
        if jsonObject == {}:
            jsonObject["subject"] = loc[len(loc)-1]
            jsonObject["classes"] = []
        else:
            num = text.split("&")[0]
            if num not in jsonObject["classes"]:
                jsonObject["classes"].append(num)
            if loc[len(loc)-1] != jsonObject["subject"]:
                arrayObj["list"].append(jsonObject)
                jsonObject = {}
                jsonObject["subject"] = loc[len(loc)-1]
                jsonObject["classes"] = []
    write("classList.json", arrayObj)

def readClassList(i=0):
    try:
     with open("classList.json", "r") as r:
	    classList = json.load(r)
     return classList
    except:
        populateTerm()
        if i is 0:
            return readClassList(1)
    print "crash or something?"
    return json.dumps({})

def cleanUp():
    print "Cleanup started"
    deleteQueue = []
    with open("jsonLayout.json", "r") as r:
	    jsonData = json.load(r)
    classList = readClassList()
    classMap = {}
    for entry in classList["list"]:
        classMap[entry["subject"]]=set(entry["classes"])
    count = 0
    for entry in jsonData["classes"]:
        if not entry["usesCRN"]:
            # if len(entry["code"]) != 3:
            #     deleteQueue.append(entry)
            #     continue
            if entry["subj"] not in classMap:
                deleteQueue.append(entry)
                continue
            elif entry["code"] not in classMap[entry["subj"]]:
                deleteQueue.append(entry)
                continue
                
        else:
            if len(entry["crn"])!=5:
                deleteQueue.append(entry)
                continue
        if "@" not in entry["email"]:
            deleteQueue.append(entry)
            continue
        if "." not in entry["email"]:
            deleteQueue.append(entry)
            continue
        if entry["sent"]:
            deleteQueue.append(entry)
            continue
    print "Amount to be deleted: " + str(len(deleteQueue))
    for obj in deleteQueue:
        jsonData["classes"].remove(obj)
        count+=1
    write("jsonLayout.json", jsonData)
    print "Ammount deleted: " + str(count)
# cleanUp()