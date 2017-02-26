########################################
## Date : 30/01/2017                  ##
## fonction : creer un fichier index  ##
## qui donne le timestamp et le nom   ##
## correspondant                      ##
##									  ##
## Notes :  1 week = 518400           ##
##			1 day  =  86400			  ##
########################################

import os
import numpy as np
import time as tm

def getTimeStamp():
	indexFile = open('dossierMeteo/index.txt','w')
	fileList = os.listdir('dossierMeteo')
	for file in fileList:
		if file[-4:]=='.bet':
			betFile = open('dossierMeteo/'+file,'r')
			line=betFile.readline()
			line=line.split(':')
			# print('{}:{}\n'.format(file,line[0]))
			indexFile.write('{}:{}\n'.format(file,line[0]))
			betFile.close()
	indexFile.close()
	
# def updateTimeStamp()
	
			
def getFilesDayDiff(indexFile,file1,file2):
## find how many days between 2 files
	DAY=86400
	WEEK=518400
	for lines in indexFile:
		lineSpl = lines.split(':')
		if lineSpl[0]==file1:
			time1 = float(lineSpl[1])
		if lineSpl[0]==file2:
			time2 = float(lineSpl[1])
	deltaDays = round(abs(time2-time1)/DAY)
	# print('{} day difference'.format(deltaDays))
	return deltaDays
	
def oneWeekFiles(fileref,nbDays):
##find files nbdays day from fileref
	DAY=86400
	indexFile = open('dossierMeteo/index.txt','r')
	OutFileList=[]
	lineSpl=[]
	##get ref time	
	for lines in indexFile:
		lineSpl.append(lines.split(':'))
		# print(lineSpl[-1][0])
		# print(fileref)
		if lineSpl[-1][0]==fileref:	
			timeRef = float(lineSpl[-1][1])
	
	##compare to ref time
	for lines in lineSpl:
		if not(lines[0]==fileref):
			time = float(lines[1])
			deltaDays = round(abs(timeRef-time)/DAY)
			if deltaDays <= nbDays:
				OutFileList.append(lines[0])			
	indexFile.close()
	return OutFileList

def NdaysDataMean(nbDays,fileRef,timePr):
##generate mean file for n days of sensors data (with a precision of timePr minutes)
	MIN=60
	MIN_TOT=1440
	  
	blockNb = np.round(MIN_TOT/timePr)
	print(blockNb)
	
	fileList = oneWeekFiles(fileRef,nbDays)
	
	fileRef = open('dossierMeteo/'+fileRef,'r')
	fileMean = open('dossierMeteo/'+str(nbDays)+'DaysAvg_meteo.abet','w')
	
	dataAvg = np.zeros((blockNb,4))	
	
	#calcul average
	cpt = np.zeros(blockNb)
	for fileNb,file in enumerate(fileList):
		# print('file \'{}\' averaged'.format(file))

		fileTemp=open('dossierMeteo/'+file,'r')
		for data in fileTemp:
			dataSpl = data.split(':') 
			time=tm.localtime(float(dataSpl[0]))
			for bl in range(blockNb):
				tMin = bl*timePr
				tMax = (bl+1)*timePr		
				formTime = time.tm_min + time.tm_hour*60
				if formTime>=tMin and formTime<tMax:
					# print('{} in [{},{}]'.format(formTime,tMin,tMax))
					for i in range(1,4):
						dataAvg[bl,i] = (dataAvg[bl,i]*(cpt[bl]) + float(dataSpl[i]))/(cpt[bl]+1)
					# if bl==20:
						# print('-I- {}eme data - Temperature : {} - moyenne : {}'.format(cpt[bl],dataSpl[1],dataAvg[bl,1]))
						# print('-I- {}'.format(file))
					cpt[bl] = cpt[bl]+1
			
	#fill time column + write file
	for bl in range(blockNb): 
		dataAvg[bl,0]=( ((bl)*timePr)*60 + ((bl+1)*timePr)*60 )/2 +(3600*23)
		# print(dataAvg[bl,0])
		fileMean.write('{}'.format(dataAvg[bl,0]))
		for i in range(1,4):
			fileMean.write(':{:.02f}'.format(dataAvg[bl,i]))
		fileMean.write('\n')
	fileMean.close()
			
			
			
			
			
			
			

# getTimeStamp()

# indexFile = open('dossierMeteo/index.txt','r')
# getFilesDayDiff(indexFile,"01-13_meteo.bet","01-15_meteo.bet")
# indexFile.close()

# print(oneWeekFiles('01-30_meteo.bet',7))

# NdaysDataMean(7,'01-30_meteo.bet',15)