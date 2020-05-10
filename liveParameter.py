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
			
			elif dataSpl[0] == 'live_exit':
				self.live_exit = int(dataSpl[1])
		paramFile.close()
		
		
	def change_value(self,type,value):
		with open('liveParameter.txt','r') as paramFile :
			lines = paramFile.readlines()
		
		with open('liveParameter.txt','w') as paramFile :
			for line in lines: 
				dataSpl = line.split('=')
				if dataSpl[0] == type:
					if dataSpl[0] == 'avgSize':
						self.avgSize = value
						
					## thresold of excluded data
					elif dataSpl[0] == 'offlimit':
						self.offlimit = value
					
					## diplay radio data on console 
					elif dataSpl[0] == 'disp':
						# print(dataSpl)
						self.disp = value
						
					elif dataSpl[0] == 'sleepTime':
						self.sleepTime = value
						
					elif dataSpl[0] == 'hist_threshold':
						self.hist_threshold = value
					
					elif dataSpl[0] == 'live_exit':
						self.live_exit = value
				
					paramFile.write('{}={}\n'.format(type,value))
				else:
					paramFile.write(line)