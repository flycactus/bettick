# -*- coding: utf-8 -*-
"""
Main routine of Bettick, home automation bot
"""

from pi_switch import RCSwitchReceiver
from passingDay import *
import numpy as np
import time
import jsonParser as json
import sendToWeb as web
from shutil import copyfile

def checksum(flag,dataNb):
	if(np.sum(flag)%2 == dataNb%2):
		return 1
	else:
		return 0
	
SLEEPING_TIME = 140

receiver = RCSwitchReceiver()
receiver.enableReceive(2)

################ Initialization ###################

# initialise la date
dateFile = open('dayfile.day','r')
today = dateFile.readline()
dateFile.close()
dataFileName = 'dossierMeteo/'+today+'_meteo.bet'
 
flag = np.zeros(6)
num=0
while True:
	if isNewDay():
		#create archive json file
		jsonFileName='dossierMeteo/'+today+'_meteo.json'
		copyfile('meteo.json', jsonFileName)
		
		#create new bet file
		today = time.strftime('%m-%d',time.localtime()) 
		dataFileName = 'dossierMeteo/'+today+'_meteo.bet'

		
	if receiver.available():
		received_value = receiver.getReceivedValue()
		if received_value:
			print received_value
			##receive temperature
			if received_value == 1:
				flag[0]=1
					
				
			elif received_value != 1 and flag[0]==1 and flag[1]==0:
				dayTemperature = received_value				
				flag[1]=1

			##receive humidity
			elif received_value == 2:
				dataNb = 2
				flag[dataNb]=1
				if not checksum(flag,dataNb):
					flag = np.zeros(6)
					
			elif received_value != 2 and flag[2]==1 and flag[3]==0:
				dayHumidity = received_value
				flag[3]=1				
				# time.sleep(SLEEPING_TIME)
				
			##receive earth humidity
			elif received_value == 3:
				dataNb = 3
				flag[dataNb]=1
				if not checksum(flag,dataNb):
					flag = np.zeros(6)
					
			elif received_value != 3 and flag[4]==1 and flag[5]==0:
				earthHumidity = received_value
				flag[5]=1				
				time.sleep(SLEEPING_TIME)
			
			
			if np.sum(flag) == 6:
				num = num+1
				flag = np.zeros(6)
				timeArray = time.time()
				dataFile = open(dataFileName,'a+')
				dataFormat = '{}:{}:{}:{}\n'.format(timeArray,dayTemperature,dayHumidity,earthHumidity)
				dataFile.write(dataFormat)
				dataFile.close()
				json.parseData()
				
				try:
					web.sendToWeb('meteo.json')
				except:
					log=open('errorLog.log','a+')
					log.write(time.strftime('%m-%d, %H:%M',time.localtime())+'Error sending json to web\n')
					log.close()
				# print 'iteration {}'.format(num)
				# print dataFormat
				
			# else:
				# print 'sum {}'.format(np.sum(flag))
				# print 'flag {} {} {} {} {} {}'.format(flag[0],flag[1],flag[2],flag[3],flag[4],flag[5])
				 
			
        receiver.resetAvailable()
