import time


dayFile = open('dayfile.day','w')
today = time.strftime('%Y-%d-%m',time.localtime()) 
print today
dayFile.write(today)
dayFile.close()