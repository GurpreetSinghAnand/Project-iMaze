from weka.classifiers import Classifier
import os

classifier = None

class DirectionClassifier(object):
	def __init__(self):
		if not os.path.exists("direction_classifier.pkl"):
			print "Classifier is not trained"
			self.train("IDR_train.arff")
			self.save("direction_classifier.pkl")
		else:
			self.load("direction_classifier.pkl")

	def train(self, trainingSet):
		global classifier		
		classifier = Classifier(name='weka.classifiers.trees.J48', ckargs={'-x':10})
		classifier.train(trainingSet, trainingSet, verbose=0)
		print "Classifier is Trained"
	
	def save(self, filename):
		global classifier
		classifier.save(filename)
		print "Classifier is Saved"
	
	def load(self, filename):
		global classifier
		classifier = Classifier.load(filename)
		print "Classifier is Loaded"
	
	def predict(self, filename):
		global classifier
		prediction_List = None
		prediction_List = list(classifier.predict(filename, verbose=1))
		length = len(prediction_List)
		prediction = prediction_List[length - 1]
		return prediction[1]


