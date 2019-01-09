import json

def write(jData):
	with open("jsonLayout.json", "w") as r:
		r.write(json.dumps(jData, sort_keys=True, indent=4, separators=(',', ':')))

def cleanUp():
    deleteQueue = []
    with open("jsonLayout.json", "r") as r:
	    jsonData = json.load(r)
    count = 0
    for entry in jsonData["classes"]:
        if not entry["usesCRN"]:
            if len(entry["code"]) != 3:
                deleteQueue.append(entry)
                continue
                #checking for valid code should go here
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
    write(jsonData)
    print "Ammount deleted: " + str(count)

cleanUp()