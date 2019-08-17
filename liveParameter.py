### parameter class, gets updated every iteration

class ParameterClass():
	def __init__(self):
		self.update()
		
	def update(self):
		paramFile = open('liveParameter.txt','r')
		# print('reading parameters')
		for line in paramFile:
			dataSpl = line.split('=')

			if dataSpl[0] == 'avgSize':
				self.avgSize = int(dataSpl[1])
				
			## thresold of excluded data
			elif dataSpl[0] == 'offlimit':
				self.offlimit = int(dataSpl[1])
			
			## diplay radio data on console 
			elif dataSpl[0] == 'disp':
				# print(dataSpl)
				self.disp = int(dataSpl[1])
				
			elif dataSpl[0] == 'sleepTime':
				self.sleepTime = int(dataSpl[1])
				
			elif dataSpl[0] == 'hist_threshold':
				self.hist_threshold = int(dataSpl[1])