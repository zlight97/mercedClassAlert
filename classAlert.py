import time
import smtplib
import requests
import datetime
import threading
import json
import cleanUp
import onionIp
import os

print "Start"
term = ''
isSpring = None
termCount = 0
deleteQueue = []
with open("jsonLayout.json", "r") as r:
	jsonData = json.load(r)

def checkTerm():
	print "Check Term called"
	global term
	global isSpring
	now = datetime.datetime.now()
	term = ''
	if now.month > 9:
		term = term + str(1+now.year)
	else:
		term = term+str(now.year)

	if now.month > 9 or now.month < 3:  # codes are 10 for spring, 20 for summer, 30 for fall, 40 for winter
		if isSpring == False:
			clearTable()
		term = term+'10'
		isSpring = True
	else:
		if isSpring == True:
			clearTable()
		term = term+'30'
		isSpring = False
	print "Check Term Finished"
	return term

def clearTable():
	global jsonData
	with open("jsonLayout.json", "r") as r:
		jsonData = json.load(r)
	jsonData["classes"][:] = []
	write(jsonData)
	print "Table cleared"
	
def makeBackup():
	filename = str(datetime.datetime.now())+".json.bkup"
	# file = open(filename, "w+")
	# f.write("")
	# f.close()
	filepath = os.path.join('~/BobcatBackups', filename)
	if not os.path.exists('~/BobcatBackups'):
		os.makedirs('~/BobcatBackups')
	with open("jsonLayout.json", "r") as r:
		backupData = json.load(r)
	with open(filepath, "w+") as r:
		r.write(json.dumps(backupData, sort_keys=True, indent=4, separators=(',', ':')))
def write(jData):
	print "Write called"
	with open("jsonLayout.json", "w") as r:
		r.write(json.dumps(jData, sort_keys=True, indent=4, separators=(',', ':')))

def inp(thread):
	stage = 0
	global jsonData
	entry = jsonData["cLayout"][0]
	while(1):
		if stage == 0:
			print("type a 3 or 4 letter class code or CRN to begin adding new. Type quit to quit")
		inp = raw_input()
		if inp == 'quit':
			break
		elif inp=='clear':
			clearTable()
		elif stage == 0 and list(inp)[0] < 'A':
			entry = jsonData["cLayout"][0]
			entry["crn"] = str(inp)
			stage = 2
			print("What is the email you would like to use?\nPhone numbers can be used as #@carrieremail.com e.g. 55555555@vtext.com")
		elif stage == 0:
			entry = jsonData["cLayout"][1]
			entry["subj"] = str(inp)
			print("What is the three didget code for the class?")
			stage = stage+1
		elif stage == 1:
			entry["code"] = str(inp)
			print("What is the email you would like to use?\nPhone numbers can be used as #@carrieremail.com e.g. 55555555@vtext.com")
			stage = stage+1
		elif stage == 2:
			entry["email"] = str(inp)
			jsonData["classes"].append(entry)
			write(jsonData)
			stage = 0



def check():
	global jsonData
	global termCount
	global deleteQueue
	while 1:
		print "Connecting to SMTP"
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(jsonData["botEmail"], jsonData["botPassword"])
		print "Sleep began"
		time.sleep(60)
		termCount = termCount+1
		if(termCount>2400):
			checkTerm()
			cleanUp.cleanUp()
			onionIp.getOnionIPList()
			termCount = 0
		with open("jsonLayout.json", "r") as r:
			jsonData = json.load(r)
		print "jsonLayout loaded"
		if len(jsonData["classes"]) == 0:
			continue
		htmlData = requests.get('https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.P_ViewSchedule?validterm='+term+'&subjcode=ALL&openclasses=Y')
		for obj in jsonData["classes"]:
			if obj["sent"]:
				continue
			elif obj["usesCRN"]:
				for st in htmlData.text.split():
					if 'crn='+obj["crn"] in st:
						server.sendmail(jsonData["botEmail"], str(obj["email"]), "There is an opening in " + str(obj["crn"]))
						print "There is an opening in " + str(obj["crn"]) + " email: "+str(obj["email"])
						obj["sent"] = True
						deleteQueue.append(obj)
						break
			elif not obj["usesCRN"]:
				for st in htmlData.text.split():
					if "subjcode="+ obj["subj"] +"&crsenumb="+obj["code"] in st:
						server.sendmail(jsonData["botEmail"], str(obj["email"]), "There is an opening in " + str(obj["subj"]) + " " + str(obj["code"]))
						print "There is an opening in " + str(obj["subj"]) + " " + str(obj["code"]) + " email: "+str(obj["email"])
						obj["sent"] = True
						deleteQueue.append(obj)
						break		
			else:
				print "JSON format INCORRECT\nTerminating Program"
				exit()
		server.quit()
		for obj in deleteQueue:
			print "removing email: "+str(obj["email"])
			jsonData["classes"].remove(obj)
		del deleteQueue[:]
		print "Writing the deleted data"
		write(jsonData)


def wrap():
	while (1):
		try:
			time.sleep(10)
			check()
		except BaseException as e:
			print(('{!r}'.format(e)))
		except SMTPServerDisconnected as excp:
			print(('{!r}'.format(excp)))
		print('Restarting thread')


if __name__ == '__main__':
	makeBackup()
	checkTerm()
	cleanUp.cleanUp()
	onionIp.getOnionIPList()
	p = threading.Thread(target=wrap)
	p.daemon = True
	p.start()
	print "Running..."
	p.join()
	#inp(p)
	print('Program sucessfully terminated')
