import pyfinch
from imageprocessing import ImageProcessing
from camera import Camera
from datarecorder import DataRecorder
from classifier import DirectionClassifier
import cv
import datetime
import time

fdr = None
class iMaze(object):
	
	now = datetime.datetime.now()
	currentDate = str(now.day)+"."+str(now.month)+"."+str(now.year)
	currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
	fdr = DataRecorder()
	fdr.openFDR()
       	startOfData = "################################# DATE: "+ currentDate + " #################################\n"
        deviceTableHeaders = "Timestamp\tDevice\t\t\t\tStatus\t\t\tValue\n"
        fdr.writeToFDR(startOfData)
	fdr.writeToFDR(deviceTableHeaders)

    	finch = pyfinch.Finch()
	now = datetime.datetime.now()
	currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        finchStatus = [currentTime+"\t\tFinch\t\t\t\tOK.\t\t\tActive\n"]
	fdr.writeToFDR(finchStatus)
	time.sleep(1.0)
        finch.led(255,0,0)
	now = datetime.datetime.now()
	currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        ledOneStatus = [currentTime+"\t\tLED_1\t\t\t\tOK.\t\t\t255,0,0 RGB\n"]
        fdr.writeToFDR(ledOneStatus)
	time.sleep(1.0)
        finch.led(0,255,0)
	now = datetime.datetime.now()
	currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        ledTwoStatus = [currentTime+"\t\tLED_2\t\t\t\tOK.\t\t\t0,255,0 RGB\n"]
        fdr.writeToFDR(ledTwoStatus)
	time.sleep(1.0)
        finch.led(0,0,255)
	now = datetime.datetime.now()
	currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        ledThreeStatus = [currentTime+"\t\tLED_3\t\t\t\tOK.\t\t\t0,0,255 RGB\n"]
        fdr.writeToFDR(ledThreeStatus)
	time.sleep(1.0)
        finch.buzzer(0.1,700)
	now = datetime.datetime.now()
	currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        buzzerStatus = [currentTime+"\t\tBuzzer\t\t\t\tOK.\t\t\t0.1s,700Hz\n"]
        fdr.writeToFDR(buzzerStatus)
	currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        thermometerStatus = [currentTime+"\t\tThermometer\t\t\tOK.\t\t\t"+ str(finch.temperature()) +" C\n"]
        fdr.writeToFDR(thermometerStatus)
	time.sleep(1.0)
        finch.wheels(1.0,0)
        time.sleep(0.1)
	now = datetime.datetime.now()
	currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        leftWheelStatus = [currentTime+"\t\tLeft Wheel\t\t\tOK.\t\t\t255m/s\n"]
        fdr.writeToFDR(leftWheelStatus)
        finch.wheels(0,1.0)
        time.sleep(0.1)
	now = datetime.datetime.now()
	currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        rightWheelStatus = [currentTime+"\t\tRight Wheel\t\t\tOK.\t\t\t255m/s\n"]
        fdr.writeToFDR(rightWheelStatus)
        finch.wheels(1.0,1.0)
        time.sleep(0.5)
	currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        accelerometerStatus = [currentTime+"\t\tAccelerometer\t\t\tOK.\t\t\t"+str(finch.acceleration())+ " m/s\n"]
        fdr.writeToFDR(accelerometerStatus)
        finch.idle()
	now = datetime.datetime.now()
	currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        finchStatus = [currentTime+"\t\tFinch\t\t\t\tOK.\t\t\tIdle\n"]
	fdr.writeToFDR(finchStatus)
	fdr.closeFDR()
       
	cam = Camera(now)
	cam.setCamera()
	cam.startCamera()
	cam.writeCameraStatus()
	imp = ImageProcessing(cam.getCamera(),now)
	while True:		
		imp.captureRGBImage()
		imp.convertRGBtoGS()
		imp.convertGStoOtsu()
		imp.generatePixelData()
		classify = DirectionClassifier()
		direction = classify.predict("IDR.arff")
		print direction		
		break
