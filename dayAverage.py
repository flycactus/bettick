########################################
## Date : 14/05/2017                  ##
## fonction : creer un fichier de data##
## qui donne les moyenne d'un capteur ##
## pour n journee                     ##
##									  ##
########################################

import numpy as np
import time
import fileTimeStamp as fts
import json 
import os

def sortFileList(fileList):
	sortArray=np.zeros((len(fileList),3))
	for i,file in enumerate(fileList):
		fileSpl=file.split('-')
		sortArray[i,0] = int(i) 
		sortArray[i,1] = fileSpl[0] 
		sortArray[i,2] = fileSpl[1][0:2]
	ind = np.lexsort((sortArray[:,1],sortArray[:,2]))
	sortArray = sortArray[ind]
	fileListSorted=[fileList[int(file)] for file in sortArray[:,0]]
	return fileListSorted

def getNdays(fileRef,oneWeekFileList):
	fileList = oneWeekFileList
	# fileList.append(fileRef)
	fileList = sortFileList(fileList)
	# print(fileList)
	avgFile = open('dossierMeteo/7DayAvgHum.abet','w')
	for file in fileList:
		
		fileTemp=open('dossierMeteo/'+file,'r')
		dataArr = []
		date0=fileTemp.readline().split(':')[0]		
		for data in fileTemp:
			dataSpl = data.split(':') 
			dataArr.append(int(dataSpl[3][:-1]))
		dataAvg = np.average(np.array(dataArr))
		# print('{} : {:.3f}'.format(file,dataAvg))
		avgFile.write('{}:{:.3f}\n'.format(date0,dataAvg))
		# print(dataAvg)
	avgFile.close()

def update_7DayAvgHum(dataFile):
	fileTemp = open(dataFile,'r')
	dataArr = []
	date0=fileTemp.readline().split(':')[0]	
	for data in fileTemp:
		dataSpl = data.split(':') 
		dataArr.append(int(dataSpl[3][:-1]))
	dataAvg = np.average(np.array(dataArr))
	
	avgFile = open('dossierMeteo/7DayAvgHum.abet','r')
	savedAvg = []
	for data in avgFile:
		savedAvg.append(data)
	# print(savedAvg)
	avgFile.close()
	
	avgFile = open('dossierMeteo/7DayAvgHum.abet','w')
	for line in range(1,len(savedAvg)):
		avgFile.write('{}\n'.format(savedAvg[line][:-1]))
	avgFile.write('{}:{:.3f}\n'.format(date0,dataAvg))		
	avgFile.close()

def toJSON(jsonFileName):
	datadict = {}
	avgFile = open('dossierMeteo/7DayAvgHum.abet','r')
	for i,line in enumerate(avgFile):
		avgSplit = line.split(':')
		datadict[i] = [float(avgSplit[0]),float(avgSplit[1][:-1])]
	json_data = (json.dumps(datadict))
	jsonFile = open(jsonFileName,'w')
	jsonFile.write(json_data)
	jsonFile.close() 	

	
def humWeekAvg(dataFile,oneWeekFileList):
	today = time.strftime('%Y-%m-%d',time.localtime())  
	if not os.path.exists('dossierMeteo/7DayAvgHum.abet'): 
		getNdays(today+'_meteo.bet',oneWeekFileList)
	else:
		update_7DayAvgHum(dataFile)
	jsonFileName='7DayAvgHum.json'
	toJSON(jsonFileName)	
	
	
	
# today = time.strftime('%m-%d',time.localtime()) 
# dataFile=today+'_meteo.bet'
# jsonFileName='7DayAvgHum.json'
# fts.getTimeStamp()
# getNdays(today+'_meteo.bet',6)	
# update_7DayAvgHum(dataFile)

# toJSON(jsonFileName)
	
	
	