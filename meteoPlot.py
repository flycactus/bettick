import time
import numpy as np
import matplotlib.pyplot as plt

###Open meteo data file
dayFile = open('dayfile.day','r')
lastDay = dayFile.readline()
dayFile.close()
meteoFileName = 'dossierMeteo/'+lastDay[:-1]+'_meteo.bet'
meteoFile = open(meteoFileName,'r')

### Extract meteo data
meteoData = meteoFile.readlines()
timeArray = np.zeros(len(meteoData))
temp = np.zeros(len(meteoData))
hum = np.zeros(len(meteoData))

for i,line in enumerate(meteoData):
	#get time
	timeEnd = line.find(':')
	timeArray[i] = line[:timeEnd]
	line = line[timeEnd+1:]

	#get temperature
	tempEnd = line.find(':')
	temp[i] = line[:tempEnd]
	line = line[tempEnd+1:]
	
	#get humidity
	humEnd = line.find(':')
	hum[i] = line[:humEnd]
	line = line[humEnd+1:]
	
print time.strftime('%H:%M',time.localtime(timeArray[1]))
plt.plot(timeArray,temp,'r')
plt.plot(timeArray,hum,'b')
plt.show()