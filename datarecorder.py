import os

finchDataRecorderFile = None
imageDataRecorderFile = None
class DataRecorder(object):
	def openFDR(self):
		global finchDataRecorderFile
		if not os.path.exists("FDR.txt"):
                	finchDataRecorderFile = open("FDR.txt", "w")
       		else:
        		finchDataRecorderFile = open("FDR.txt", "a+")

	def openIDR(self):
		global  imageDataRecorderFile
		if not os.path.exists("IDR.arff"):
                	imageDataRecorderFile = open("IDR.arff", "w")
			schema = ["@relation direction"+"\n\n"+"@attribute redpixelinfirstblock numeric"+"\n"+"@attribute redpixelinsecondblock numeric"+"\n"+"@attribute redpixelinthirdblock numeric"+"\n"+"@attribute redpixelinfourthblock numeric"+"\n"+"@attribute redpixelinfifthblock numeric"+"\n"+"@attribute redpixelinsixthblock numeric"+"\n"+"@attribute redpixelinseventhblock numeric"+"\n"+"@attribute redpixelineightblock numeric"+"\n"+"@attribute redpixelinninthblock numeric"+"\n"+"@attribute redpixelintenthblock numeric"+"\n"+"@attribute redpixelineleventhblock numeric"+"\n"+"@attribute redpixelintwelvethblock numeric"+"\n"+"@attribute redpixelinthirteenthblock numeric"+"\n"+"@attribute redpixelinfourteenthblock numeric"+"\n"+"@attribute redpixelinfifteenthblock numeric"+"\n"+"@attribute redpixelinsixteenthblock numeric"+"\n"+"@attribute class"+"\t"+"{RT,LT,TJ,CJ,ST}"+"\n\n"+"@data"+"\n"]
			self.writeToIDR(schema)

        	'''else:
        		imageDataRecorderFile = open("IDR.arff", "a+")
			#imageDataRecorderFile = open("IDR_train.arff", "a+")'''
	
	def writeToFDR(self, data):
		global finchDataRecorderFile
		finchDataRecorderFile.writelines(data)

	def writeToIDR(self, data):
		global imageDataRecorderFile
		imageDataRecorderFile.writelines(data)

	def closeFDR(self):
		global finchDataRecorderFile
		finchDataRecorderFile.close()
	def closeIDR(self):
		global imageDataRecorderFile
		imageDataRecorderFile.close()
	
