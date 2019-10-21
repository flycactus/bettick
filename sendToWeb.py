# -*- coding: utf-8 -*-
"""
Send data to raspi.sarno.fr
"""

from ftplib import FTP
import os

def sendToWeb(fileName,filePath,destPath=''):
	id=open('../id','r')
	idStr = id.read()
	idStr = idStr.split(':')
	# print(idStr)
	ftp = FTP(idStr[2])     # connect to host, default port
	ftp.login(idStr[0],idStr[1])   

	ftp.cwd('www')            	
	ftp.cwd('raspi') 
	# ftp.retrlines('LIST')           # list directory contents
	ftp.cwd(destPath) 
	upload(ftp,fileName,filePath)
	# print('transfert fini')
	ftp.quit()

def upload(ftp, fileName,filePath):
    ext = os.path.splitext(fileName)[1]
    if ext in (".txt", ".htm", ".html"): 
        ftp.storlines("STOR " + fileName, open(filePath+fileName))
    else:
        ftp.storbinary("STOR " + fileName, open(filePath+fileName, "rb"), 1024)
		
		

# sendToWeb('17-04-11_14.jpeg','/home/cactus/bettick/photo/')