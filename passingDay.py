import time

def isNewDay():
	dayFile = open('dayfile.day','r')
	lastDay = dayFile.readline()
	dayFile.close()
	today = time.strftime('%m-%d',time.localtime()) 
	if today != lastDay:
		dayFile = open('dayfile.day','w')
		dayFile.write(today)
		dayFile.close()
		return 1
	else:
		return 0