import csv
import random
import math
import operator
import sys
import numpy
import matplotlib.pyplot as plot

def loadFold(fold, classifier, dataset=[], trainingSet=[] , testSet=[]):
	arr=[0]*10
	sda=[[],[],[],[],[]]
	divider=len(dataset)/fold
	for i in range(0,fold):		
		testSet=dataset[i*divider:(i+1)*divider]
		trainingSet=dataset[0:i*divider]+dataset[(i+1)*divider:len(dataset) - 1]
		for k in range(1,6):
			predictions=[]
			for x in range(0,len(testSet)):
				# print testSet[x]
				neighbors = getNeighbors(trainingSet, testSet[x], k,classifier)
				result = getResponse(neighbors,classifier)
				predictions.append(result)
			accuracy = getAccuracy(testSet, predictions,classifier)
			arr[k]+=accuracy
			sda[k-1].append(accuracy)
			#print('Accuracy: ' + repr(accuracy) + '%'+' for KNN: '+str(k))
	mean=numpy.array(arr)	
	mean=mean/fold	
	print "Mean:\n"
	print mean[1:6] 
	s1=numpy.std(numpy.array(sda[0]))
	s2=numpy.std(numpy.array(sda[1]))
	s3=numpy.std(numpy.array(sda[2]))
	s4=numpy.std(numpy.array(sda[3]))
	s5=numpy.std(numpy.array(sda[4]))
	print "Standard Deviations:"
	standardD =[s1,s2,s3,s4,s5]
	print standardD
	plot.title("Fold # : %d" % fold)
	plot.errorbar(range(1,6),mean[1:6],xerr=0,yerr=standardD)
	plot.xlabel('K-value')
	plot.ylabel('Mean Accuracy')
	plot.ylim([20,100])
	plot.xlim([0,6])
	nm=str(fold)+".png"
	plot.savefig(str(nm))
	#plot.close()
	plot.show()
	

def euclideanDistance(instance1, instance2, length, ignore_it):
	distance = 0
	for x in range(length):
		if not x == ignore_it:
			distance += pow(float(instance1[x]) - float(instance2[x]), 2)
	return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k,classifier):
	distances = []
	length = len(testInstance)
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length,classifier)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def getResponse(neighbors,classifier):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][classifier]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

def getAccuracy(testSet, predictions,classifier):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][classifier] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0	

def main():
	trainingSet=[]
	testSet=[]
	filename=sys.argv[1]
	classifier = int(sys.argv[2])
	with open(filename, 'rb') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    random.shuffle(dataset)
	try:
		dataset.remove([])
	except:
		pass
	#random.shuffle(dataset)
	for fold in range(2,6):
		print "Fold # ",fold
		loadFold(fold, classifier, dataset, trainingSet, testSet)

main()