# -*- coding: utf-8 -*-
"""
Send data to raspi.sarno.fr
"""

from ftplib import FTP
import os

def sendToWeb(file='meteo2.json'):
	id=open('../id','r')
	idStr = id.read()
	idStr = idStr.split(':')
	# print idStr
	ftp = FTP(idStr[2])     # connect to host, default port
	ftp.login(idStr[0],idStr[1])   

	ftp.cwd('www')            
	# ftp.retrlines('LIST')           # list directory contents
	ftp.cwd('raspi') 
	upload(ftp,file)
	# print 'transfert fini'
	ftp.quit()

def upload(ftp, file):
    ext = os.path.splitext(file)[1]
    if ext in (".txt", ".htm", ".html"): 
        ftp.storlines("STOR " + file, open(file))
    else:
        ftp.storbinary("STOR " + file, open(file, "rb"), 1024)
		
		
sendToWeb('meteo.json')