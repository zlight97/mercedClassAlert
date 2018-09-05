import time
import smtplib
import requests
import datetime
import threading

now = datetime.datetime.now()
term = ''
terminate = False
if now.month>9:
	term = term + str(1+now.year)
else:
	term = term+str(now.year)

if now.month>9 or now.month<3:#codes are 10 for spring, 20 for summer, 30 for fall, 40 for winter
	term = term+'10'
else:
	term = term+'30'

def writeFile(filename, line, message):
	with open(filename, 'r') as f:
		wr = f.readlines()
	wr[line] = message
	with open(filename,'w') as f:
		f.writelines(wr)

def inp(thread):
	global terminate
	stage = 0
	entry = []
	entry.append('%\n')
	entry.append('N\n')
	while(1):
		# if p.isAlive() == False:
			# p.start()
		if stage==0:
			print("type a 3 or 4 letter code or CRN to begin adding new. Type quit to quit")
		inp = raw_input()
		if inp == 'quit':
			terminate = True
			break
		elif stage == 0 and list(inp)[0]<'A':
			entry.append(str(inp)+"\n")
			entry.append("FILLED\n")
			stage = 2
			print("What is the email you would like to use?\nPhone numbers can be used as #@carrieremail.com e.g. 55555555@vtext.com")
		elif stage == 0:
			print("What is the three didget code for the class?")
			stage = stage+1
			entry.append(str(inp)+'\n')
		elif stage == 1:
			print("What is the email you would like to use?\nPhone numbers can be used as #@carrieremail.com e.g. 55555555@vtext.com")
			stage = stage+1
			entry.append(str(inp) + '\n')
		elif stage == 2:
			stage = 0
			entry.append(str(inp) + '\n')
			entry.append('#END\n')
			with open('classList.txt', 'r') as f:
				wr = f.readlines()
			a = len(wr)-1
			wr[a] = entry[0]
			for b in range (1,6):
				wr.append(entry[b])
			with open('classList.txt','w') as f:
				f.writelines(wr)

skip = ''
pos = 0
code = ''
num = ''
email = ''
cur = []

with open('classList.txt') as f:
	cur = f.read().splitlines()

def nextPos(cPos):
	global skip
	global code
	global num
	global email
	global cur
	if '#END' in cur[cPos]:
		with open('classList.txt') as f:
			cur = f.read().splitlines()
			cPos = 0
	if 'SKIP' in cur[cPos+1]:
		skip = 1
	code = cur[cPos+2]
	num = cur[cPos+3]
	email = cur[cPos+4]
	cPos = cPos+5
	return cPos
	
pos = nextPos(pos)
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("email@gmail.com", "password")#CHANGE ME
crnTbl = requests.get('https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.P_ViewSchedule?validterm='+term+'&subjcode=ALL&openclasses=Y')
def getCRNtbl():
	global term
	global crnTbl
	while(1):
		global crnTbl
		url = 'https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.P_ViewSchedule?validterm='+term+'&subjcode=ALL&openclasses=Y'
		crnTbl = requests.get(url)
		time.sleep(30)

def crn(number):
	global crnTbl
	global term
	crnStr = 'crn='+str(number)
	for st in crnTbl.text.split():
		if crnStr in st:
			msg = "There is an opening in "+number
			print(msg)
			server.sendmail("email@gmail.com",email,msg)#CHANGE ME
			cur[pos-4] = 'SKIP'
			writeFile('classList.txt',pos-4,'SKIP\n')
			break
	if '#END' in cur[pos]:
		time.sleep(60)
		crnTbl = requests.get('https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.P_ViewSchedule?validterm='+term+'&subjcode=ALL&openclasses=Y')


def run():
	global term
	global pos
	global crnTbl
	while (1):
		time.sleep(5)
		if terminate:
			break
		if 'SKIP' in cur[pos-4]:
			if '#END' in cur[pos]:
				time.sleep(60)
				crnTbl = requests.get('https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.P_ViewSchedule?validterm='+term+'&subjcode=ALL&openclasses=Y')
			pos = nextPos(pos)
			continue
		if list(code)[0] < 'A':
			crn(code)
			pos = nextPos(pos)
			continue
		url = 'https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.P_ViewSchedule?validterm='+term+'&subjcode='+code+'&openclasses=Y' #validterm will need to change based on term, could make part of text file, but easy enough to deal with
		r = requests.get(url)
		check = "crsenumb="+num+"&"
		for string in r.text.split():
			if check in string:
				msg = "There is an opening in "+code+" "+num
				print(msg)
				server.sendmail("email@gmail.com",email,msg)#CHANGE ME
				cur[pos-4] = 'SKIP'
				writeFile('classList.txt',pos-4,'SKIP\n')
				break
		if '#END' in cur[pos]:
			time.sleep(60)
			crnTbl = requests.get('https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.P_ViewSchedule?validterm='+term+'&subjcode=ALL&openclasses=Y')
		pos = nextPos(pos)
def wrap():
	while (1):
		try:
			time.sleep(10)
			run()
		except BaseException as e:
			print(('{!r}'.format(e)))
		else:
			print('Restarting thread')
if __name__ == '__main__':
    p = threading.Thread(target=wrap)
    p.daemon = True
    p.start()
    inp(p)
server.quit()
print('1')
