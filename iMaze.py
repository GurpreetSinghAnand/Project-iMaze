import pyfinch
from imageprocessing import ImageProcessing
from camera import Camera
from datarecorder import DataRecorder
import cv

class iMaze(object):
	
	now = datetime.datetime.now()
	currentDate = str(now.day)+"."+str(now.month)+"."+str(now.yea
	fdr = DataRecorder(now)
       	startOfData = "################################# DATE: "+ currentDate + " #################################\n"
        deviceTableHeaders = "Timestamp\tDevice\t\t\t\tStatus\t\t\tValue\n"
        fdr.writeToFDR(startOfData)
	fdr.writeToFDR(deviceTableHeaders)

    	finch = pyfinch.Finch()
        finchStatus = ["\t\tFinch\t\t\t\tOK.\t\t\tActive\n"]
	fdr.writeToFDR(finchStatus)
	time.sleep(1.0)
        finch.led(255,0,0)
        ledOneStatus = ["\t\tLED_1\t\t\t\tOK.\t\t\t255,0,0 RGB\n"]
        fdr.writeToFDR(ledOneStatus)
	time.sleep(1.0)
        finch.led(0,255,0)
        ledTwoStatus = ["\t\tLED_2\t\t\t\tOK.\t\t\t0,255,0 RGB\n"]
        fdr.writeToFDR(ledTwoStatus)
	time.sleep(1.0)
        finch.led(0,0,255)
        ledThreeStatus = ["\t\tLED_3\t\t\t\tOK.\t\t\t0,0,255 RGB\n"]
        fdr.writeToFDR(ledThreeStatus)
	time.sleep(1.0)
        finch.buzzer(0.1,700)
        buzzerStatus = ["\t\tBuzzer\t\t\t\tOK.\t\t\t0.1s,700Hz\n"]
        fdr.writeToFDR(buzzerStatus)
        thermometerStatus = ["\t\tThermometer\t\t\tOK.\t\t\t"+ str(finch.temperature()) +" C\n"]
        fdr.writeToFDR(thermometerStatus)
	time.sleep(1.0)
        finch.wheels(1.0,0)
        time.sleep(0.1)
        leftWheelStatus = ["\t\tLeft Wheel\t\t\tOK.\t\t\t255m/s\n"]
        fdr.writeToFDR(leftWheelStatus)
        finch.wheels(0,1.0)
        time.sleep(0.1)
        rightWheelStatus = ["\t\tRight Wheel\t\t\tOK.\t\t\t255m/s\n"]
        fdr.writeToFDR(rightWheelStatus)
        finch.wheels(1.0,1.0)
        time.sleep(0.5)
        accelerometerStatus = ["\t\tAccelerometer\t\t\tOK.\t\t\t"+str(finch.acceleration())+ " m/s\n"]
        fdr.writeToFDR(accelerometerStatus)
        finch.idle()
        finchStatus = ["\t\tFinch\t\t\t\tOK.\t\t\tIdle\n"]
	fdr.writeToFDR(finchStatus)
	fdr.closeFDR()
       
	cam = Camera()
	cam.setCamera()
	cam.startCamera()
	cam.writecameraStatus()
	imp = ImageProcessing(cam.getCamera(),dataFile,now)
	while True:		
		imp.captureRGBImage()
		imp.convertRGBtoGS()
		imp.convertGStoOtsu()
