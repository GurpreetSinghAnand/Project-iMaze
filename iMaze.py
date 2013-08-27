import pyfinch
from imageprocessing import ImageProcessing
import pygame.camera
import datetime
import time

class iMaze(object):
	
	now = datetime.datetime.now()
	currentDate = str(now.day)+"."+str(now.month)+"."+str(now.year)
    	currentTime = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
	dataFile = open("FDR.txt","a+")
       	startOfData = "################################# DATE: "+ currentDate + " #################################\n"
        deviceTableHeaders = "Timestamp\tDevice\t\t\t\tStatus\t\t\tValue\n"
        dataFile.writelines(startOfData)
        dataFile.writelines(deviceTableHeaders)
    	finch = pyfinch.Finch()
    	#if pyfinch.FinchConnection.is_open(finch):
        finchStatus = [currentTime,"\t\tFinch\t\t\t\tOK.\t\t\tActive\n"]
	dataFile.writelines(finchStatus)
	time.sleep(1.0)
        finch.led(255,0,0)
        ledOneStatus = [currentTime,"\t\tLED_1\t\t\t\tOK.\t\t\t255,0,0 RGB\n"]
        dataFile.writelines(ledOneStatus)
	time.sleep(1.0)
        finch.led(0,255,0)
        ledTwoStatus = [currentTime,"\t\tLED_2\t\t\t\tOK.\t\t\t0,255,0 RGB\n"]
        dataFile.writelines(ledTwoStatus)
	time.sleep(1.0)
        finch.led(0,0,255)
        ledThreeStatus = [currentTime,"\t\tLED_3\t\t\t\tOK.\t\t\t0,0,255 RGB\n"]
        dataFile.writelines(ledThreeStatus)
	time.sleep(1.0)
        finch.buzzer(0.1,700)
        buzzerStatus = [currentTime,"\t\tBuzzer\t\t\t\tOK.\t\t\t0.1s,700Hz\n"]
        dataFile.writelines(buzzerStatus)
        thermometerStatus = [currentTime,"\t\tThermometer\t\t\tOK.\t\t\t"+ str(finch.temperature()) +" C\n"]
        dataFile.writelines(thermometerStatus)
	time.sleep(1.0)
        finch.wheels(1.0,0)
        time.sleep(0.1)
        leftWheelStatus = [currentTime,"\t\tLeft Wheel\t\t\tOK.\t\t\t255m/s\n"]
        dataFile.writelines(leftWheelStatus)
        finch.wheels(0,1.0)
        time.sleep(0.1)
        rightWheelStatus = [currentTime,"\t\tRight Wheel\t\t\tOK.\t\t\t255m/s\n"]
        dataFile.writelines(rightWheelStatus)
        finch.wheels(1.0,1.0)
        time.sleep(0.5)
        accelerometerStatus = [currentTime,"\t\tAccelerometer\t\t\tOK.\t\t\t"+str(finch.acceleration())+ " m/s\n"]
        dataFile.writelines(accelerometerStatus)
        finch.idle()
        finchStatus = [currentTime,"\t\tFinch\t\t\t\tOK.\t\t\tIdle\n"]
	dataFile.writelines(finchStatus)
        #else:
        	#finchStatus = [currentTime,"\t\tFinch\t\tNot Connected.\t\t\tInactive\n"]
       	 	#sys.exit(0)
        
	pygame.camera.init()
	camera = pygame.camera.Camera(pygame.camera.list_cameras()[0])
	camera.start()	
	imp = ImageProcessing(camera,dataFile,now)
	imp.cameraStatus()
	while True:		
		imp.captureRGBImage()
		imp.convertRGBtoGS()
		imp.convertGStoOtsu()
