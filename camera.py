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
    
    