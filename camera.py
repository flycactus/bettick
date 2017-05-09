## Bibliotheque pour le control de la camera

import picamera as cam
import time
import os



def initCam():
	camera = cam.PiCamera()
	return camera
	
def takePhoto(camera,fileName):
	camera.capture(fileName)

	
def timeLapse_Photo(photoTaken_flag):
	now = time.strftime('%H',time.localtime()) 
	fileName = ''
	filePath = ''
	hourArray=['{:02d}'.format(x) for x in range(8,22,2)] 
	flagOffArray = ['{:02d}'.format(x) for x in range(9,23,2)]
	
	if now in hourArray and photoTaken_flag == 0:
		camera = initCam()
		today = time.strftime('%y-%m-%d',time.localtime())  
		filePath = 'photo/'
		fileName = today+'_{}.jpeg'.format(now)
		camera.capture(filePath+fileName)
		photoTaken_flag=1
		camera.close()
		
	if now in flagOffArray:
		photoTaken_flag=0
		

	return [fileName,filePath,photoTaken_flag]
	
def makeGif():
	today = time.strftime('%y-%m-%d',time.localtime())
	os.system('convert -delay 30 -loop 0 photo/{}*.jpeg animation.gif'.format(today)) 
	os.system('convert -delay 30 -loop 0 photo/*_12.jpeg animation12.gif'.format(today)) 
	
	