import requests
import time


def postToWeb(strTime,temp,hum,sensor):
	addresse = "http://raspi.sarno.fr/add_data_db.php"
	try:
		# payload_tuples = [('time', '2020-02-01 20:29:20'), ('temp', '18.5'), ('hum', '55'), ('sensor', '1')]
		payload_tuples = [('time', strTime), ('temp', temp), ('hum', hum), ('sensor', sensor)]
		r1 = requests.post(addresse, data=payload_tuples)
	except Exception as e:
		log=open('errorLog.log','a+')
		log.write(time.strftime('%Y-%m-%d, %H:%M',time.localtime())+' - Error posting to web : {}\n'.format(e))
		log.close()

