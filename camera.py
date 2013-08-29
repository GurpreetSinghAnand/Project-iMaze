import pygame.camera
from datarecorder import DataRecorder
import datetime

camera = None
fdr = None
now = None
currentTime = None
class Camera(object):
	def __init__(self, now):
		self.now = now
		currentTime = str(self.now.hour)+":"+str(self.now.minute)+":"+str(self.now.second)
		pygame.camera.init()

	def setCamera(self):
		global camera
		camera = pygame.camera.Camera("/dev/video0",(800,600))

	def getCamera(self):
		global camera
		return camera

	def startCamera(self):
		global camera
		camera.start()

	def stopCamera(self):
		global camera
		camera.stop()

	def writeCameraStatus(self):
		global camera
		global now
		fdr = DataRecorder()
		fdr.openFDR()
       		if camera is None:
			now = datetime.datetime.now()
			currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        	    	camStatus = [currentTime+"\t\tCamera\t\t\t\tNot Connected.\t\t\tInactive\n"]
			sys.exit(0)
        	else:
			now = datetime.datetime.now()
			currentTime = str(self.now.hour)+":"+str(self.now.minute)+":"+str(self.now.second)
            		camStatus = [currentTime+"\t\tCamera\t\t\t\tOK.\t\t\tActive\n"]

    		fdr.writeToFDR(camStatus)
		fdr.closeFDR()
