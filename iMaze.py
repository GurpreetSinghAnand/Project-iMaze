import pyfinch
from imageprocessing import ImageProcessing
import pygame.camera
import datetime

class iMaze(object):
	
	now = datetime.datetime.now()
	currentDate = str(now.day)+"."+str(now.month)+"."+str(now.year)		
	dataFile = open("FDR.txt","a+")
	startOfData = "#################### DATE: "+ currentDate + " ####################\n"
	dataFile.writelines(startOfData)

	pygame.camera.init()
	camera = pygame.camera.Camera(pygame.camera.list_cameras()[0])
	camera.start()	
	imp = ImageProcessing(camera,dataFile,now)
	imp.cameraStatus()
	while True:		
		imp.captureRGBImage()
		imp.convertRGBtoGS()
		imp.convertGStoOtsu()