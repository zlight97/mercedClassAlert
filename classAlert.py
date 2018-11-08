import time
import smtplib
import requests
import datetime
import threading
import json

term = ''
isSpring = None
termCount = 0
deleteQueue = []
with open("jsonLayout.json", "r") as r:
	jsonData = json.load(r)

def checkTerm():
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

def clearTable():
	global jsonData
	with open("jsonLayout.json", "r") as r:
		jsonData = json.load(r)
	jsonData["classes"][:] = []
	write(jsonData)
	
def write(jData):
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
		time.sleep(60)
		termCount = termCount+1
		if(termCount>2400):
			checkTerm()
			termCount = 0
		with open("jsonLayout.json", "r") as r:
			jsonData = json.load(r)
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
						print "There is an opening in " + str(obj["crn"])
						obj["sent"] = True
						deleteQueue.append(obj)
						break
			elif not obj["usesCRN"]:
				for st in htmlData.text.split():
					if "subjcode="+ obj["subj"] +"&crsenumb="+obj["code"] in st:
						server.sendmail(jsonData["botEmail"], str(obj["email"]), "There is an opening in " + str(obj["subj"]) + " " + str(obj["code"]))
						print "There is an opening in " + str(obj["subj"]) + " " + str(obj["code"])
						obj["sent"] = True
						deleteQueue.append(obj)
						break		
			else:
				print "JSON format INCORRECT\nTerminating Program"
				exit()
		for obj in deleteQueue:
			jsonData["classes"].remove(obj)
                del deleteQueue[:]
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
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(jsonData["botEmail"], jsonData["botPassword"])

		else:
			print('Restarting thread')


if __name__ == '__main__':
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(jsonData["botEmail"], jsonData["botPassword"])
	checkTerm()
	p = threading.Thread(target=wrap)
	p.daemon = True
	p.start()
	inp(p)
server.quit()
print('Program sucessfully terminated')
