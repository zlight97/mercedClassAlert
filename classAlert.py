import time
import smtplib
import requests



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
	url = 'https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.P_ViewSchedule?validterm=201810&subjcode='+code+'&openclasses=Y' #validterm will need to change based on term, could make part of text file, but easy enough to deal with
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
