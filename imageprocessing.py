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

counter = 0
fdr = None
idr = None
fileAddresses = None
image_Data = None
imgh = 0
RGB_path = "/home/gurpreet/Desktop/RGB/"
GS_path = "/home/gurpreet/Desktop/GS/"
Otsu_path = "/home/gurpreet/Desktop/Otsu/"
class ImageProcessing(object):

	def __init__(self,camera, now):
		global fdr
		self.camera =  camera
		self.now = now
		fdr = DataRecorder()
		if not os.path.exists(RGB_path):
    			os.makedirs(RGB_path)
		if not os.path.exists(GS_path):
    			os.makedirs(GS_path)
		if not os.path.exists(Otsu_path):
    			os.makedirs(Otsu_path)
	
	def captureRGBImage(self):
		global counter
		global fdr
		fdr.openFDR()
    		counter = counter + 1
		image = self.camera.get_image()
		pygame.image.save(image, RGB_path+str(counter)+".jpg")
		camUpdateStatus = ["\t\tCamera\t\t\t\tCapturing.\t\t\t"+RGB_path+str(counter)+".jpg"+"\n"]
		fdr.writeToFDR(camUpdateStatus)

	def convertRGBtoGS(self):
		global counter
		global fdr
		image = Image.open(RGB_path+str(counter)+".jpg")
        	imageGS = ImageOps.grayscale(image)
		imageGS=imageGS.convert()
        	imageGS.save(GS_path+str(counter)+".jpg")
		camUpdateStatus = ["\t\tCamera\t\t\t\tConverting.\t\t\t"+GS_path+str(counter)+".jpg"+"\n"]
		fdr.writeToFDR(camUpdateStatus)

	def convertGStoOtsu(self):
		global counter
		global fdr
		imageOtsu = mahotas.imread(GS_path+str(counter)+".jpg", as_grey=True)	
		imageOtsu= imageOtsu.astype(np.uint8)
        	ThresholdOtsu = mahotas.otsu(imageOtsu)
		print ThresholdOtsu
		ax = pylab.axes([0,0,1,1], frameon=False)
        	ax.set_axis_off()
        	im = pylab.imshow(imageOtsu > ThresholdOtsu)
        	pylab.savefig(Otsu_path+str(counter)+".jpg")
		camUpdateStatus = ["\t\tCamera\t\t\t\tConverting.\t\t\t"+Otsu_path+str(counter)+".jpg"+"\n"]
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
        image_Data[colnum] = "%0.4f" % (100 * float(total_Red_Pixel / total_Pixel_In_Cell))    	

	def generatePixelData(self):
    	global imgh
        global image_Data
	global Otsu_path
        address = Otsu_path+str(counter)+".jpg"
	imgh = 0
    	colnum = 0
    	cell_Height = 0
    	current_Cell_Height = 0
        image = Image.open(address)
        imwidth, imheight = image.size
        pix = image.load()
        impix = (126, 0, 0)
        image_Data = [0 for i in xrange(4)]
        cell_Height = imheight * 0.25
        current_Cell_Height = current_Cell_Height + cell_Height
        self.countRedPixels(imwidth, current_Cell_Height, colnum, impix, pix)
        colnum = colnum + 1
        current_Cell_Height = current_Cell_Height + cell_Height
        self.countRedPixels(imwidth, current_Cell_Height, colnum, impix, pix)
        colnum = colnum + 1
        current_Cell_Height = current_Cell_Height + cell_Height
        self.countRedPixels(imwidth, current_Cell_Height, colnum, impix, pix)
        colnum = colnum + 1
        current_Cell_Height = current_Cell_Height + cell_Height
        self.countRedPixels(imwidth, current_Cell_Height, colnum, impix, pix)
        colnum = 0

        direction = raw_input("Enter a Direction Acronym: ")
            data = " "
            while colnum<4:
                    data = data + str(image_Data[i])+"\t"
		    colnum = colnum + 1
	    if direction == "LT":
            	data = data + "\t" + str(2)
	    elif direction == "TJ":
		data = data + "\t" + str(3)
	    elif direction == "CJ":
		data = data + "\t" + str(4)
	    elif direction == "ST":
		data = data + "\t" + str(5)
	    else:
		data = data + "\t" + str(1)

            dataFile.writelines(data+"\n")
	    image_Data = None
        dataFile.close()

		
