import pygame.camera
from datarecorder import DataRecorder

camera = None
fdr = None
class Camera(object):
	def __init__(self):
		global camera
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
		fdr = DataRecorder()
		fdr.openFDR()
       		if self.camera is None:
        	    	camStatus = ["\t\tCamera\t\t\t\tNot Connected.\t\t\tInactive\n"]
			sys.exit(0)
        	else:
            		camStatus = ["\t\tCamera\t\t\t\tOK.\t\t\tActive\n"]

    		fdr.writeToFDR(camStatus)
		fdr.closeFDR()
