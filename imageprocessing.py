import numpy as np
import mahotas
import pylab
import pygame.camera
import pygame.image
from PIL import Image
from PIL import ImageOps
import cv
import cv2
import datetime
import sys

class ImageProcessing(object):

	def __init__(self,camera, dataFile, now):
		self.camera =  camera
		self.dataFile = dataFile
		self.now = now
		
	
	def cameraStatus(self):
		if self.dataFile is None:
                	self.dataFile = open("FDR.txt", "w")
        	else:
        		self.dataFile = open("FDR.txt", "a+")
			currentTime = str(self.now.hour)+":"+str(self.now.minute)+":"+str(self.now.second)
       		if self.camera is None:
        	    	camStatus = [currentTime,"\t\tCamera\t\t\t\tNot Connected.\t\t\tInactive\n"]
			sys.exit(0)
        	else:
            		camStatus = [currentTime,"\t\tCamera\t\t\t\tOK.\t\t\tActive\n"]

    		self.dataFile.writelines(camStatus)
	
	def captureRGBImage(self):
		#self.camera.start()
		image = self.camera.get_image()
		pygame.image.save(image, "RGB.jpg")

	def convertRGBtoGS(self):
		image = Image.open("RGB.jpg")
        	imageGS = ImageOps.grayscale(image)
		imageGS=imageGS.convert()
        	imageGS.save("GS.jpg")

	def convertGStoOtsu(self):
		imageOtsu = mahotas.imread("GS.jpg", as_grey=True)	
		imageOtsu= imageOtsu.astype(np.uint8)
        	ThresholdOtsu = mahotas.otsu(imageOtsu)
		ax = pylab.axes([0,0,1,1], frameon=False)
        	ax.set_axis_off()
        	im = pylab.imshow(imageOtsu > ThresholdOtsu)
        	pylab.savefig("Otsu.jpg")
		iplOtsu = cv.LoadImage("Otsu.jpg")
        	cv.ShowImage("iMaze", iplOtsu)
	def 
