import csv
import random
import math
import operator
import numpy

def loadFold(fold, dataset=[], trainingSet=[] , testSet=[]):
	divider=len(dataset)/fold
	mean = [[0 for x in range(0,6)] for x in range(0,6)]
	for i in range(0,fold):		
		testSet=dataset[i*divider:(i+1)*divider]
		trainingSet=dataset[0:i*divider]+dataset[(i+1)*divider:len(dataset) - 1]		
		for k in range(1,6):
			predictions=[]
			for x in range(0,len(testSet)):
				# print testSet[x]
				neighbors = allNeighbours(trainingSet, testSet[x], k)
				result = analysis(neighbors)
				predictions.append(result)
			accuracy = Stats(testSet, predictions)
			#print "Adding:"+str(accuracy)+"+"+str(mean[k][fold])
			mean[k][fold]=float(accuracy)+mean[k][fold]		
			#print('Accuracy: ' + str(accuracy) + '%'+' for KNN: '+str(k)+' & fold: '+str(fold)+ ' & subset: '+str(i))
	ar=numpy.array(mean)
	ar=ar/fold
	print ar
	#print "K=2, Mean Values are:", (ar[1][2],ar[2][2],ar[3][2],ar[3][3],ar[3][4])
			




def Dist(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

def allNeighbours(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = Dist(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(0,k):
		neighbors.append(distances[x][0])
	return neighbors

def analysis(neighbors):
	feedback = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in feedback:
			feedback[response] += 1
		else:
			feedback[response] = 1
	sortedVotes = sorted(feedback.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

def Stats(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0	

def main():
	trainingSet=[]
	testSet=[]
	filename='iris.data'
	with open(filename, 'rb') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(1,len(dataset[0])-1):
	            dataset[x][y] = float(dataset[x][y])
	#random.shuffle(dataset)
	for fold in range(2,6):
		print "-----------------------------------------------------Fold # ",fold
		loadFold(fold, dataset, trainingSet, testSet)

main()