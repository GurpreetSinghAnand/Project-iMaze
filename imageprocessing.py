import numpy as np
import mahotas
import pylab
import pygame.camera
import pygame.image
from PIL import Image
from PIL import ImageOps
import cv
import cv2
import os
import glob
from datarecorder import DataRecorder
import datetime

counter = 0
fdr = None
idr = None
now = None
currentTime = None
fileAddresses = None
image_Data = None
imgh = 0
RGB_path = "RGB/"
GS_path = "GS/"
Otsu_path = "Otsu/"
class ImageProcessing(object):

	def __init__(self,camera, now):
		global fdr
		global idr
		global currentTime
		self.camera =  camera
		self.now = now
		fdr = DataRecorder()
		idr = DataRecorder()
		if not os.path.exists(RGB_path):
    			os.makedirs(RGB_path)
		if not os.path.exists(GS_path):
    			os.makedirs(GS_path)
		if not os.path.exists(Otsu_path):
    			os.makedirs(Otsu_path)
	
	def captureRGBImage(self):
		global counter
		global fdr
		global now
		fdr.openFDR()
    		counter = counter + 1
		image = self.camera.get_image()
		pygame.image.save(image, RGB_path+str(counter)+".jpg")
		now = datetime.datetime.now()
		currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
		camUpdateStatus = [currentTime+"\t\tCamera\t\t\t\tCapturing.\t\t"+RGB_path+str(counter)+".jpg"+"\n"]
		fdr.writeToFDR(camUpdateStatus)

	def convertRGBtoGS(self):
		global counter
		global fdr
		global now
		image = Image.open(RGB_path+str(counter)+".jpg")
        	imageGS = ImageOps.grayscale(image)
		imageGS=imageGS.convert()
        	imageGS.save(GS_path+str(counter)+".jpg")
		now = datetime.datetime.now()
		currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
		camUpdateStatus = [currentTime+"\t\tCamera\t\t\t\tConverting.\t\t"+GS_path+str(counter)+".jpg"+"\n"]
		fdr.writeToFDR(camUpdateStatus)

	def convertGStoOtsu(self):
		global counter
		global fdr
		global now
		imageOtsu = mahotas.imread(GS_path+str(counter)+".jpg", as_grey=True)	
		imageOtsu= imageOtsu.astype(np.uint8)
        	ThresholdOtsu = mahotas.otsu(imageOtsu)
		ax = pylab.axes([0,0,1,1], frameon=False)
        	ax.set_axis_off()
        	im = pylab.imshow(imageOtsu > ThresholdOtsu)
        	pylab.savefig(Otsu_path+str(counter)+".jpg")
		now = datetime.datetime.now()
		currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
		camUpdateStatus = [currentTime+"\t\tCamera\t\t\t\tConverting.\t\t"+Otsu_path+str(counter)+".jpg"+"\n"]
		fdr.writeToFDR(camUpdateStatus)	
		fdr.closeFDR()
		self.generatePixelData()
	
    	def countRedPixels(self, imwidth, current_Cell_Height, colnum, impix, pix):
		global imgh        
    		global image_Data
		total_Red_Pixel = 0
        	total_Pixel_In_Cell = 0
	
        	while imgh< current_Cell_Height:
            		imgw=0
            		while imgw<imwidth:
                		if pix[imgw,imgh] == impix:
                    			total_Red_Pixel = total_Red_Pixel + 1
                    			total_Pixel_In_Cell = total_Pixel_In_Cell + 1
                		else:
                    			total_Pixel_In_Cell = total_Pixel_In_Cell + 1
                		imgw = imgw + 1
            		imgh = imgh + 1
			if total_Pixel_In_Cell != 0:
				image_Data[colnum] = "%0.4f" % (100 * float(total_Red_Pixel / total_Pixel_In_Cell))
			else:
				image_Data[colnum] = 0.000    	

	def generatePixelData(self):
		global counter
		global idr
		global image_Data
    		global imgh
		global previous_Height
		global previous_Width
		idr = DataRecorder()
	    	imgh = 0
    	    	colnum = 0
    	    	cell_Height = 0
    	    	current_Cell_Height = 0
	    	cell_Width = 0
    	    	current_Cell_Width = 0
	    	address = Otsu_path+str(counter)+".jpg"
            	image = Image.open(address)
            	imwidth, imheight = image.size
            	pix = image.load()
            	impix = (126, 0, 0)
            	image_Data = [0 for i in xrange(16)]
            	cell_Height = imheight * 0.25
	    	cell_Width = imwidth * 0.25
            	current_Cell_Height = current_Cell_Height + cell_Height #150
	    	current_Cell_Width = current_Cell_Width + cell_Width #200
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
	    	colnum = colnum + 1
	    	current_Cell_Width = current_Cell_Width + cell_Width #400
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
            	colnum = colnum + 1
	    	current_Cell_Width = current_Cell_Width + cell_Width #600
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
            	colnum = colnum + 1
	    	current_Cell_Width = current_Cell_Width + cell_Width #800
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
	    	previous_Height = imgh #150
	    	previous_Width = 0
	    	current_Cell_Width = 0
	    	current_Cell_Height = current_Cell_Height + cell_Height #300
	    	current_Cell_Width = current_Cell_Width + cell_Width #200
	    	colnum = colnum + 1
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
            	colnum = colnum + 1
	    	current_Cell_Width = current_Cell_Width + cell_Width #400
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
            	colnum = colnum + 1
	    	current_Cell_Width = current_Cell_Width + cell_Width #600
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
            	colnum = colnum + 1
	    	current_Cell_Width = current_Cell_Width + cell_Width #800
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
	    	previous_Height = imgh
	    	previous_Width = 0
	    	current_Cell_Width = 0
	    	current_Cell_Height = current_Cell_Height + cell_Height #450
	    	current_Cell_Width = current_Cell_Width + cell_Width #200
	    	colnum = colnum + 1
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
            	colnum = colnum + 1
	    	current_Cell_Width = current_Cell_Width + cell_Width #400
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
            	colnum = colnum + 1
	    	current_Cell_Width = current_Cell_Width + cell_Width #600
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
            	colnum = colnum + 1
	    	current_Cell_Width = current_Cell_Width + cell_Width #800
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
	    	previous_Height = imgh
	    	previous_Width = 0
	    	current_Cell_Width = 0
	    	current_Cell_Height = current_Cell_Height + cell_Height #600
	    	current_Cell_Width = current_Cell_Width + cell_Width #200
	    	colnum = colnum + 1
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
            	colnum = colnum + 1
	    	current_Cell_Width = current_Cell_Width + cell_Width #400
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
            	colnum = colnum + 1
	    	current_Cell_Width = current_Cell_Width + cell_Width #600
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
            	colnum = colnum + 1
	    	current_Cell_Width = current_Cell_Width + cell_Width #800
            	self.countRedPixels(current_Cell_Width, current_Cell_Height, colnum, impix, pix)
	    	previous_Height = imgh
	    	previous_Width = 0
	    	colnum = 0
	    	idr.openIDR()
		data = ""
            	while colnum<16:
                	data = data + str(image_Data[colnum])+","
			colnum = colnum + 1
	    	data = data + "?\n"
            	idr.writeToIDR(str(data))
	    	terminators = "%\n%\n%"
	    	idr.writeToIDR(terminators)
	    	image_Data = None
	    	colnum = 0
            	idr.closeIDR()

		
