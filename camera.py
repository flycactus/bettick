## Bibliotheque pour le control de la camera

import picamera as cam
import time
import os
import ultraSound as usd
from shutil import copyfile
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def initCam():
    camera = cam.PiCamera()
    return camera
    
def takePhoto(camera,fileName):
    camera.capture(fileName)

def triggeredPic(parameter):
	timeStamp = time.strftime("%Y_%m_%d_%H-%M",time.localtime())
	filePath = 'photo/'
	
	dist = usd.distance()
	dist2 = -10
	if dist<35:	
		dist2 = usd.distance()
	if parameter.disp==1:
		print('dist = {} - dist2 = {}'.format(int(dist),int(dist2)))
	if np.abs(dist-dist2) < 5:
		fileName = 'trigPic_{}_{}_{}_0.jpeg'.format(timeStamp,int(dist),int(dist2))
		while os.path.exists(filePath+fileName):
			photoNb = int(fileName[-6:-5])
			fileName = fileName[:-6]+str(photoNb+1)+'.jpeg'
			
		camera = initCam()
		takePhoto(camera,filePath+fileName)
		# print('Photo taken({:.1f}cm) {}'.format(dist,fileName))
		camera.close()
		return fileName
	return 0
	
def histCompareTrig(parameter):
	bins = 50
	delta_threshold = parameter.hist_threshold
	
	new_bird = 0
	
	current_filePath = 'photo/current.jpeg'
	camera = initCam()
	takePhoto(camera,current_filePath)
	camera.close()
	
	current_pic = plt.imread(current_filePath, format='jpeg') 
	hist = np.histogram(current_pic,bins) 
	
	previous_filePath = 'photo/previous.jpeg' 
	previous_pic = plt.imread(previous_filePath, format='jpeg')
	hist2 = np.histogram(previous_pic,bins)
	
	## measure the difference between histograms
	delta = np.sum(np.abs(hist[0]-hist2[0]))
	
	## change ref file
	copyfile(current_filePath,previous_filePath)
	if parameter.disp == 1:
		print('delta hist {}'.format(delta))
		
	if delta > delta_threshold:
		timeStamp = time.strftime("%Y_%m_%d_%H-%M",time.localtime())
		filePath = 'photo/'
		fileName = 'trigPic_{}_0.jpeg'.format(timeStamp)
		new_bird = fileName
		
		##save file into web
		os.rename(current_filePath,filePath+fileName)
	
	## return 0 if no new file or filePath otherwise
	return new_bird
		
def timeLapse_Photo(photoTaken_flag):
    hour = time.strftime('%H',time.localtime()) 
    minut = time.strftime('%M',time.localtime()) 
    fileName = ''
    filePath = ''
    hourArray=['{:02d}'.format(x) for x in range(8,22,2)] 
    minutArray=['{:02d}'.format(x) for x in range(0,60,10)] 
    flagOffArray = ['{:02d}'.format(x) for x in range(5,60,2)]
    
    if hour in hourArray and minut in minutArray and photoTaken_flag == 0:
        camera = initCam()
        today = time.strftime('%y-%m-%d',time.localtime())  
        filePath = 'photo/'
        filePath = filePath+today   
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            
        fileName = today+'_{}.jpeg'.format(hour+'h'+minut)
        camera.capture(filePath+fileName)
        photoTaken_flag=1
        camera.close()
        
    if minut in flagOffArray:
        photoTaken_flag=0
         
    return [fileName,filePath,photoTaken_flag]
    
def makeGif():
    today = time.strftime('%y-%m-%d',time.localtime())
    os.system('convert -delay 30 -loop 0 photo/{}/{}*.jpeg animation.gif'.format(today,today)) 
    os.system('convert -delay 30 -loop 0 photo/{}/*_12.jpeg animation12.gif'.format(today,today)) 
    
    