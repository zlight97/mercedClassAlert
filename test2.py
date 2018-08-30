def inp():
	stage = 0
	entry = []
	entry.append('%\n')
	entry.append('N\n')
	while(1):
		if stage==0:
			print("type a 3 or 4 letter code to begin adding new. Type quit to quit")
		inp = raw_input()
		if inp == quit:
			break
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
inp()