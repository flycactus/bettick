# -*- coding: utf-8 -*-
"""
Main routine of Bettick, home automation bot
"""

from pi_switch import RCSwitchReceiver
from passingDay import *
import liveParameter as param
import numpy as np
import time
import jsonParser as json
import sendToWeb as web
from shutil import copyfile
import sys
import fileTimeStamp as fts


class sensorDataClass:
	def __init__(self):
		self.dayTemperature = 0
		self.dayHumidity = 0
		self.earthHumidity = 0
		self.randomId = 0
		self.checksum = 0
		self.sum = 0
		self.valid = 0
		self.histo = [0,0,0,0]
		
	def reinit(self):
		self.dayTemperature = 0
		self.dayHumidity = 0
		self.earthHumidity = 0
		self.randomId = 0
		self.checksum = 0
		
	def reinitStat(self):
		self.sum = 0
		self.valid = 0
		self.histo = [0,0,0,0]
	
	def disp(self):
		print('temp:{}*C\nhumidity:{}%\nrandomId:{}\nearthHum:{}\nchecksum:{}'.format(self.dayTemperature,self.dayHumidity,self.randomId,self.earthHumidity,self.checksum))
		print(time.strftime('%H:%M:%S',time.localtime())+'\n')
		


def saveStat(summ,valid,histo):
	statFile = open('./stat/stat_'+time.strftime('%m-%d',time.localtime())+'.st','w')
	statFile.write('#Trames Totales                 : {}\n'.format(summ))
	statFile.write('#Trames Valides                 : {} ({:.2f} %)\n'.format(valid,float(valid)/float(summ)*100))
	statFile.write('#Trames 1 - Temperature         : {} (x{:.2f})\n'.format(histo[0],float(histo[0])/float(summ)))
	statFile.write('#Trames 2 - Humidite & random Id: {} (x{:.2f})\n'.format(histo[1],float(histo[1])/float(summ)))
	statFile.write('#Trames 3 - Humidite terre      : {} (x{:.2f})\n'.format(histo[2],float(histo[2])/float(summ)))
	statFile.write('#Trames 4 - Checksum            : {} (x{:.2f})\n'.format(histo[3],float(histo[3])/float(summ)))
	statFile.close()

	
def checksumCmp(sensorData):
	sum = sensorData.dayTemperature + sensorData.dayHumidity + sensorData.randomId + sensorData.earthHumidity
	if(sum == sensorData.checksum):
		return 1
	else:
		return 0
		
def decode(received_value,sensorData):
    valid = 0
    messageNb = int(received_value[0])
   
    if messageNb == 1:
		sensorData.dayTemperature = int(received_value[1:4])
		# sensorData.histo[0] = sensorData.histo[0]+1
    if messageNb == 2:
        sensorData.dayHumidity = int(received_value[1:3])
        sensorData.randomId = int(received_value[3:4])
        # sensorData.histo[1] = sensorData.histo[1]+1
    if messageNb == 3:
		sensorData.earthHumidity = int(received_value[1:4])
		# sensorData.histo[2] = sensorData.histo[2]+1
    if messageNb == 4:
		sensorData.checksum = int(received_value[1:4])
		# sensorData.histo[3] = sensorData.histo[3]+1
		# print('{}+{}+{} = {}'.format(sensorData.dayTemperature,sensorData.dayHumidity,sensorData.earthHumidity,sensorData.dayTemperature + sensorData.dayHumidity + sensorData.earthHumidity))
		if sensorData.dayTemperature + sensorData.dayHumidity + sensorData.earthHumidity != 0:
			# sensorData.disp()
			sensorData.sum = sensorData.sum + 1
			if(checksumCmp(sensorData)):
				valid=1
				sensorData.valid = sensorData.valid +1
				saveStat(sensorData.sum,sensorData.valid,sensorData.histo)
				# print "==> valide {}/{} ({} %)".format(sensorData.valid,sensorData.sum,float(sensorData.valid)/float(sensorData.sum)*100)
			else:
				sensorData.reinit()
		else:
			sensorData.reinit()
			
    return sensorData,valid
	
	
def sendToRaspiWeb(file):
	try:
		web.sendToWeb(file)
	except Exception as e:
		log=open('errorLog.log','a+')
		log.write(time.strftime('%m-%d, %H:%M',time.localtime())+' - Error sending json to web : {}\n'.format(e))
		log.close()
	# print('sleep '+time.strftime('%H:%M:%S',time.localtime()))
	time.sleep(SLEEPING_TIME)
	

receiver = RCSwitchReceiver()
receiver.enableReceive(2)

################ Initialization ###################

# initialisation des erreurs
fsock = open('errorLog.log', 'a')               
sys.stderr = fsock       

# initialisation des parametres
parameter = param.ParameterClass()
SLEEPING_TIME = parameter.sleepTime

# initialise la date
dateFile = open('dayfile.day','r')
today = dateFile.readline()
dateFile.close()
dataFileName = 'dossierMeteo/'+today+'_meteo.bet'

# initialise la classe
sensorData = sensorDataClass()
flag = np.zeros(6)
num=0
while True:
	
	if isNewDay():
		#create archive json file
		jsonFileName='dossierMeteo/'+today+'_meteo.json'
		copyfile('meteo.json', jsonFileName) 
		sensorData.reinitStat()
		
		#compute last week file
		fts.getTimeStamp()
		NbofDays = 7
		TimePrecision = 10   
		fts.NdaysDataMean(NbofDays,today+'_meteo.bet',TimePrecision)
		avgFileNameBet = 'dossierMeteo//{}DaysAvg_meteo.abet'.format(NbofDays)
		avgFileNameJson= '{}DaysAvg_meteo.json'.format(NbofDays)
		json.parseData(avgFileNameBet,avgFileNameJson,parameter)		
		sendToRaspiWeb(avgFileNameJson)

		
		#create new bet file
		today = time.strftime('%m-%d',time.localtime()) 
		dataFileName = 'dossierMeteo//'+today+'_meteo.bet'
		
		
	
	if receiver.available():
		parameter.update()
		received_value = receiver.getReceivedValue()

			
		if received_value:
		
			#check if the received strhas the good length
			received_value=str(received_value)
			if len(received_value)<4: 
				received_value = '9999'
			trameNb = int(received_value[0])
			if trameNb>0 and trameNb<=4:	
				sensorData.histo[trameNb-1] = sensorData.histo[trameNb-1]+1
			[sensorData,valid] = decode(received_value,sensorData)
			
			
			
			if valid: 
				if parameter.disp==1:
					sensorData.disp()
				timeArray = time.time()
				dataFile = open(dataFileName,'a+')
				dataFormat = '{}:{}:{}:{}\n'.format(timeArray,sensorData.dayTemperature,sensorData.dayHumidity,sensorData.earthHumidity)
				dataFile.write(dataFormat)
				dataFile.close()
				# jsonize today file
				json.parseData(dataFileName,'meteo.json',parameter)
				sensorData.reinit()
				
				# send to web
				sendToRaspiWeb('meteo.json')
				
				# print('fin de sleep '+time.strftime('%H:%M:%S',time.localtime())+'\n')
				# print 'iteration {}'.format(num)
				# print dataFormat
				
			# else:
				# print 'sum {}'.format(np.sum(flag))
				# print 'flag {} {} {} {} {} {}'.format(flag[0],flag[1],flag[2],flag[3],flag[4],flag[5])
				 
			
        receiver.resetAvailable()
