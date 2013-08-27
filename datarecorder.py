finchDataRecorderFile = None
imageDataRecorderFile = None
now = None
currentDate = None
currentTime = None
class DataRecorder(object):
	def __init__(self, now):
	self.now = now
    	currentTime = str(self.now.hour)+":"+str(self.now.minute)+":"+str(self.now.second)
	

	def openFDR(self):
		global finchDataRecorderFile
		if not os.path.exists("FDR.txt"):
                	finchDataRecorderFile = open("FDR.txt", "w")
       		else:
        		finchDataRecorderFile = open("FDR.txt", "a+")

	def openIDR(self):
		global  imageDataRecorderFile
		if not os.path.exists("IDR.txt"):
                	imageDataRecorderFile = open("IDR.txt", "w")
        	else:
        		imageDataRecorderFile = open("IDR.txt", "a+")

	'''def accessFDR(self):
		global finchDataRecorderFile
		return finchDataRecorderFile

	def accessIDR(self):
		global imageDataRecorderFile
		return imageDataRecorderFile'''
	
	def writeToFDR(self, data):
		global finchDataRecorderFile
		global currentTime
		finchDataRecorderFile.writelines(currentTime+data)

	def writeToIDR(self, data):
		global imageDataRecorderFile
		global currentTime
		imageDataRecorderFile.writelines(currentTime+data)

	def closeFDR(self):
		global finchDataRecorderFile
		finchDataRecorderFile.close()
	def closeIDR(self):

	def writeToIDR(self, data)
		global imageDataRecorderFile
		imageDataRecorderFile.writelines(data)
	
