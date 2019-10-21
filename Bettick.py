# -*- coding: utf-8 -*-
"""
Main routine of Bettick, home automation bot
"""

from pi_switch import RCSwitchReceiver
from passingDay import *
import liveParameter as param
import camera as cam
import numpy as np
import time
import jsonParser as json
import sendToWeb as web
import dayAverage
from shutil import copyfile
import sys
import fileTimeStamp as fts
import struct
import ultraSound 

# initialisation des parametres
parameter = param.ParameterClass()

SHORT_SLEEPING_TIME = 0.5
class sensorDataClass:
	def __init__(self):
		self.dayTemperature = 0
		self.tempOk = 0
		self.dayHumidity = 0
		self.humOk = 0
		self.randomId = 0
		self.checksum = 0
		self.dataComplete = 0
		self.earthHumidity = 0
		self.sum = 0
		self.valid = 0
		self.histo = [0,0,0,0,0] ## #0 = temp ok, #1 = hum ok, #2 = bad checksum, #3 complete, #4 total
		
	def reinit(self):
		self.dayTemperature = 0
		self.dayHumidity = 0
		self.earthHumidity = 0
		self.randomId = 0
		self.checksum = 0
		self.tempOk = 0
		self.humOk = 0
		self.valid = 0
		self.dataComplete = 0
		
	def reinitStat(self):
		self.sum = 0
		self.valid = 0
		self.histo = [0,0,0,0,0]
	
	def __repr__(self):
		out = 'temp:{}*C\nhumidity:{}%\n'.format(self.dayTemperature,self.dayHumidity)
		# out = out + 'TempOk:{}\nHumOk:{}\ndataComplete:{}\n'.format(self.tempOk,self.humOk,self.dataComplete)
		out = out + time.strftime('%H:%M:%S',time.localtime())+'\n'
		return out


def saveStat(histo,sensorData):
	if sensorData.watchdog < 20:
		statFile = open('./stat/stat_'+time.strftime('%Y-%m-%d',time.localtime())+'.st','w')
		statFile.write('#Trames Totales                 : {}\n'.format(histo[4]))
		statFile.write('#Trames Completes validees      : {}\n'.format(histo[3]))
		statFile.write('#Trames Non Valides             : {} ({:.2f} %)\n'.format(histo[2],float(histo[2])/float(histo[4])*100))
		statFile.write('#Trames 1 - Temperature         : {} ({:.2f} %)\n'.format(histo[0],float(histo[0])/float(histo[4])*100))
		statFile.write('#Trames 2 - Humidite            : {} ({:.2f} %)\n'.format(histo[1],float(histo[1])/float(histo[4])*100))
		statFile.close()
		
	if sensorData.dataComplete == 1:
		sensorData.watchdog = 0
	else :
		sensorData.watchdog += 1
		
	if parameter.disp==1: 
		print(histo)
		print(sensorData.watchdog)
	
def checksumCmp(sensorData):
	sum = sensorData.dayTemperature + sensorData.dayHumidity + sensorData.randomId + sensorData.earthHumidity
	if(sum == sensorData.checksum): 
		return 1
	else:
		return 0
		
def decode(received_value,sensorData):
	valid = 0
   # decode byte3
	byte3 = (0xFF000000 & received_value) >> 24
	typeID = int((0xF0 & byte3) >> 4)
	sensorID = int((0x0F & byte3))

	# decode byte2 and byte1
	data = int((0x00FFF000 & received_value) >> 12)

	# decode byte0
	checkSum = int((0x00000FF0 & received_value) >> 4)
	randNb   = int((0x0000000F & received_value))
	calculatedCheckSum = 0x0FF & (typeID + sensorID + data+ randNb)
	
	if calculatedCheckSum!=checkSum:
		valid = 0
		## upgrade stat bad checksum
		sensorData.histo[2]+=1
		return sensorData,valid
		
	elif typeID == 1 : # Temperature data
		sensorData.dayTemperature = float(data)/10
		sensorData.tempOk = 1
		## upgrade stat temp
		sensorData.histo[0]+=1
		
	elif typeID == 2:  #Humidity data
		sensorData.dayHumidity = float(data)/10
		sensorData.humOk = 1
		## upgrade stat hum
		sensorData.histo[1]+=1
		
	valid=1
			
	sensorData.dataComplete = sensorData.humOk & sensorData.tempOk
	saveStat(sensorData.histo,sensorData)
	
	return sensorData,valid
	
	
def sendToRaspiWeb(fileName,filePath,destPath=''):
	try:
		web.sendToWeb(fileName,filePath,destPath) 
	except Exception as e:
		log=open('errorLog.log','a+')
		log.write(time.strftime('%Y-%m-%d, %H:%M',time.localtime())+' - Error sending json to web : {}\n'.format(e))
		log.close()
	# print('sleep '+time.strftime('%H:%M:%S',time.localtime()))

	


################ Initialization ###################

# initialization radio
receiver = RCSwitchReceiver()
receiver.enableReceive(2)


## initialisation des erreurs

# set error to be written in file
fsock = open('errorLog.log', 'w')               
sys.stderr = fsock       


SLEEPING_TIME = parameter.sleepTime

# initialise la date
dateFile = open('dayfile.day','r')
today = dateFile.readline()
dateFile.close()
dataFileName = 'dossierMeteo/'+today+'_meteo.bet'

# initialise la classe
sensorData = sensorDataClass()
sensorData.watchdog = 0
flag = np.zeros(6)
num=0

# initialise la camera
photoTaken_flag=0

#raed parameter at initialization
parameter.update()

# init short sleep counter (wait signal_ready)
short_sleep_cnt = 0

if parameter.disp==1:
	print('Initialization complete')


while True: 
	
	if isNewDay():
		try:
			#create archive json file
			jsonFileName='dossierMeteo/'+today+'_meteo.json'
			copyfile('meteo.json', jsonFileName) 
			sensorData.reinitStat()
			
			#compute last week file
			fts.getTimeStamp()
			NbofDays = 7
			TimePrecision = 10   
			oneWeekFileList = fts.NdaysDataMean(NbofDays,today+'_meteo.bet',TimePrecision)
			avgFileNameBet = 'dossierMeteo//{}DaysAvg_meteo.abet'.format(NbofDays)
			avgFileNameJson= '{}DaysAvg_meteo.json'.format(NbofDays)
			json.parseData(avgFileNameBet,avgFileNameJson,parameter)		
			sendToRaspiWeb(avgFileNameJson,'')

			#Compute and send 7DayAvgHum files (.abet & .json)
			dayAverage.humWeekAvg(dataFileName,oneWeekFileList)
			jsonFileName='7DayAvgHum.json'
			sendToRaspiWeb(jsonFileName,'')
			
			#create new bet file
			today = time.strftime('%Y-%m-%d',time.localtime()) 
			dataFileName = 'dossierMeteo//'+today+'_meteo.bet'
		except Exception as error:
			print('{}'.format(error))
			fsock.write('{}'.format(error))
			pass
		  
	if receiver.available():
		parameter.update()
		received_value = receiver.getReceivedValue()
		
		if received_value:
		
			short_sleep_cnt = 0
			
			## upgrade total received_value
			sensorData.histo[4]+=1
			
			##decode the data and check its integrity
			[sensorData,valid] = decode(received_value,sensorData)
			
			if valid==1 and sensorData.dataComplete==1: 
				## upgrade total validated value
				sensorData.histo[3]+=1
				if parameter.disp==1:
					print(sensorData)
					print(dataFileName)
				timeArray = time.time()
				dataFile = open(dataFileName,'a+')
				dataFormat = '{}:{}:{}:{}\n'.format(timeArray,sensorData.dayTemperature,sensorData.dayHumidity,sensorData.earthHumidity)
				dataFile.write(dataFormat)
				dataFile.close()
				## jsonize today file
				json.parseData(dataFileName,'meteo.json',parameter)
				sensorData.reinit()
				
				## send to web
				sendToRaspiWeb('meteo.json','')
				
				if parameter.disp==1:
					print('START SLEEP')
				time.sleep(SLEEPING_TIME)
				if parameter.disp==1:
					print('STOP SLEEP')
			

			
			
			time.sleep(0.1)

	now = time.strftime('%H',time.localtime())       

	# print('test Pic')
	# try :
		# if int(now) < 20 and int(now) > 6: 
			# parameter.update()	
			# trigPic_name = cam.triggeredPic(parameter)
			# if trigPic_name != 0:
				# sendToRaspiWeb(trigPic_name,'/home/cactus/bettick/photo/','trigPic') 
				# if parameter.disp==1:
					# print('photo triggerered')
	# except KeyboardInterrupt:
		# print("Measurement stopped by User")
		# GPIO.cleanup()	
	short_sleep_cnt+=1
	time.sleep(SHORT_SLEEPING_TIME)
	if parameter.disp==1:
		if short_sleep_cnt%10 == 0:
			print('{} times SHORT_SLEEP'.format(short_sleep_cnt))
	
	##take picture
	# [fileName,filePath,photoTaken_flag] = cam.timeLapse_Photo(photoTaken_flag)
	
	## GIF
	
	# if now == '21':					
		# cam.makeGif()
		# sendToRaspiWeb('animation.gif','') 
		# sendToRaspiWeb('animation12.gif','')
		
		# receiver.resetAvailable()
	
	# time.sleep(SLEEPING_TIME)
	# time.sleep(0.0)