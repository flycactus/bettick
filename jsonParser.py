import json 
import time
import numpy as np


def parseData(betFile,jsonFileName,parameter):
	AVG_SIZE = parameter.avgSize
	# OFFLIMIT = 0.15
	OFFLIMIT = parameter.offlimit 
	##Open meteo data file
	# dayFile = open('dayfile.day','r')
	# lastDay = dayFile.readline()
	# dayFile.close()  
	# meteoFileName = 'dossierMeteo/'+lastDay+'_meteo.bet'
	meteoFile = open(betFile,'r')

	### Extract meteo data
	jsonFile = open(jsonFileName,'w')
	datadict = {}
	meteoData = meteoFile.readlines()
	time = np.zeros(len(meteoData))
	temp = np.zeros(len(meteoData))
	tempPrint = np.zeros(len(meteoData))
	hum = np.zeros(len(meteoData))
	humPrint = np.zeros(len(meteoData))
	earth = np.zeros(len(meteoData))
	earthPrint = np.zeros(len(meteoData))



	for i,line in enumerate(meteoData):
		dataTemp = [float(x) for x in line.split(':')]
		time[i] = dataTemp[0]

	
		if i==0:	
			temp[i] = dataTemp[1]
			hum[i] = dataTemp[2]
			earth[i] = dataTemp[3]
		else:		
			if i> AVG_SIZE:
				backAvg = AVG_SIZE
			else:
				backAvg = i
				
			
			avgTemp = np.average(temp[i-backAvg:i])
			stdTemp = avgTemp*OFFLIMIT
			
			
			avgHum = np.average(hum[i-backAvg:i])
			stdHum = avgHum*OFFLIMIT

			avgEarth = np.average(earth[i-backAvg:i])
			stdEarth = avgEarth*OFFLIMIT

			# print '{}-{}={}'.format(dataTemp[1],avgTemp,dataTemp[1]-avgTemp)
			# print 3*stdTemp
			# print temp[i-backAvg:i]
			# print "==========================================="
			if np.abs(dataTemp[1]-avgTemp)<3*stdTemp:  
				temp[i] = dataTemp[1]
			else:
				temp[i] = avgTemp

			if np.abs(dataTemp[2]-avgHum)<3*stdHum:  
				hum[i] = dataTemp[2]
			else:
				hum[i] = avgHum

			if np.abs(dataTemp[3]-avgEarth)<3*stdEarth:   
				earth[i] = dataTemp[3]
			else:
				earth[i] = avgEarth
			
		if i<AVG_SIZE-1: 
			# print "i:"+str(i)
			for point in range(int(np.floor(i/2))+1):
				tempPrint[i-point] = round(np.average(temp[i-point-i/2:i+1]),3)
				
				humPrint[i-point] = round(np.average(hum[i-point-i/2:i+1]),3)
				earthPrint[i-point] = round(np.average(earth[i-point-i/2:i+1]),3)
				# print "{} = [{}:{}] = {}".format(i-point,i-point-i/2,i-point+AVG_SIZE/2,tempPrint[i-point])

		elif i>=AVG_SIZE-1:
			# print "i:"+str(i) 
			for point in range(AVG_SIZE/2):
				# if i<25:
					# print "[{}:{}]".format(i-point-AVG_SIZE/2,i-point+AVG_SIZE/2)
				tempPrint[i-point] = round(np.average(temp[i-point-AVG_SIZE/2:i-point+AVG_SIZE/2]),3)
				# print(tempPrint[i-point])
				humPrint[i-point] = round(np.average(hum[i-point-AVG_SIZE/2:i-point+AVG_SIZE/2]),3)
				earthPrint[i-point] = round(np.average(earth[i-point-AVG_SIZE/2:i-point+AVG_SIZE/2]),3)
		
		
	for i in range(len(meteoData)):
		datadict[i] = [time[i],tempPrint[i],humPrint[i],earthPrint[i]]
	json_data = (json.dumps(datadict))
	jsonFile.write(json_data)
	jsonFile.close() 	
 
	
# parseData()
	
	
	