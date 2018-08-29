import time
import smtplib
import requests
import datetime

now = datetime.datetime.now()
term = ''

if now.month>9:
	term = term + str(1+now.year)
else:
	term = term+str(now.year)

if now.month>9 or now.month<3:#codes are 10 for spring, 20 for summer, 30 for fall, 40 for winter
	term = term+'30'
else:
	term = term+'10'

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
        if '#END' in cur[cPos]:
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
server.login("email@gmail.com", "password")
while (1):
	time.sleep(60)
	url = 'https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.P_ViewSchedule?validterm='+term+'&subjcode='+code+'&openclasses=Y' #validterm will need to change based on term, could make part of text file, but easy enough to deal with
	print(url)
	r = requests.get(url)
	check = "crsenumb="+num+"&"
	print(check)
	for string in r.text.split():
		if check in string:
			msg = "There is an opening in "+code+" "+num
			print(code)
			server.sendmail("email@gmail.com",email,msg)
			print(email)
			cur[pos-4] = 'SKIP'
			break
	pos = nextPos(pos)
	if pos == 0:
		time.sleep(60)
server.quit()
print('1')
