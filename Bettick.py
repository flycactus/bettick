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


class sensorDataClass:
	def __init__(self):
		self.dayTemperature = 0
		self.dayHumidity = 0
		self.earthHumidity = 0
		self.randomId = 0
		self.checksum = 0
		
	def reinit(self):
		self.dayTemperature = 0
		self.dayHumidity = 0
		self.earthHumidity = 0
		self.randomId = 0
		self.checksum = 0
	
	def disp(self):
		print('temp:{}*C\nhumidity:{}%\nrandomId:{}\nearthHum:{}\nchecksum:{}'.format(self.dayTemperature,self.dayHumidity,self.earthHumidity,self.randomId,self.checksum))

		
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
    if messageNb == 2:
        sensorData.dayHumidity = int(received_value[1:3])
        sensorData.randomId = int(received_value[3:4])
    if messageNb == 3:
		sensorData.earthHumidity = int(received_value[1:4])
    if messageNb == 4:
		sensorData.checksum = int(received_value[1:4])
		if(checksumCmp(sensorData)):
			valid=1
    return sensorData,valid
	
SLEEPING_TIME = 140

receiver = RCSwitchReceiver()
receiver.enableReceive(2)

################ Initialization ###################

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
		
		#create new bet file
		today = time.strftime('%m-%d',time.localtime()) 
		dataFileName = 'dossierMeteo/'+today+'_meteo.bet'

		
	if receiver.available():
		received_value = receiver.getReceivedValue()
		if received_value:
			received_value=str(received_value)
			# print '{}'.format(received_value)
			[sensorData,valid] = decode(received_value,sensorData)
			
			
			
			if valid:
				# sensorData.disp()
				timeArray = time.time()
				dataFile = open(dataFileName,'a+')
				dataFormat = '{}:{}:{}:{}\n'.format(timeArray,sensorData.dayTemperature,sensorData.dayHumidity,sensorData.earthHumidity)
				dataFile.write(dataFormat)
				dataFile.close()
				json.parseData()
				sensorData.reinit()
				try:
					web.sendToWeb('meteo.json')
				except Exception as e:
					log=open('errorLog.log','a+')
					log.write(time.strftime('%m-%d, %H:%M',time.localtime())+' - Error sending json to web : {}\n'.format(e))
					log.close()
				# print 'iteration {}'.format(num)
				# print dataFormat
				
			# else:
				# print 'sum {}'.format(np.sum(flag))
				# print 'flag {} {} {} {} {} {}'.format(flag[0],flag[1],flag[2],flag[3],flag[4],flag[5])
				 
			
        receiver.resetAvailable()
