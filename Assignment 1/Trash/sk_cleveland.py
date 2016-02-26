import csv
import random
import math
import operator
import matplotlib.pyplot as plot

def Kfold(dataset, num,k):
  avg = len(dataset) / float(num)
  out = []
  last = 0.0
  i =0
  accuracy=[]
  while last < len(dataset):
  	if (i==0):
  		accuracy.append(knn(k,dataset[int(last+avg):len(dataset)],dataset[int(last):int(last + avg)]))
  	elif (i==(num-1)):
  		accuracy.append(knn(k,dataset[0:int(last)],dataset[int(last):len(dataset)]))
  	else:
  		accuracy.append(knn(k,dataset[0:int(last)]+dataset[int(last+avg):len(dataset)],dataset[int(last):int(last+avg)]))

    	last += avg
    	i = i+1
  mean = round(sum(accuracy)/len(accuracy),2)
  std = round(euclideanDistance(accuracy,[mean]*len(accuracy),len(accuracy))/math.sqrt(len(accuracy)),2)
  return [mean,std]
 

def loadDataset(filename):
	with open(filename, 'rb') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)):
	        for y in range(12):
	        	try:
					dataset[x][y] = float(dataset[x][y])
	        	except: 
					dataset[x][y] = 0
	    random.shuffle(dataset)
	    return dataset
 
 
def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		try:
			distance += pow((instance1[x] - instance2[x]), 2)
		except:
			pass
	return math.sqrt(distance)
 
def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors
 
def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]
 
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

def knn(k,trainingSet,testSet):
	predictions=[]
	for x in range(len(testSet)):
		neighbors = getNeighbors(trainingSet, testSet[x], k)
		result = getResponse(neighbors)
		predictions.append(result)
		#print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
	accuracy = getAccuracy(testSet, predictions)	
	return accuracy


def main():
	return_list=[]
	m=[]
	std=[]
	mean_values={}
	std_values = {}
	dataset = loadDataset('cleveland.data.txt')
	for i in range(2,6):
		print('No of folds:'+ str(i))
		for j in range(1,6):
			print(j)
			print('[Mean, Standard Deviation]=' + str(Kfold(dataset,i,j)))
			return_list= Kfold(dataset,i,j)
			std_values[j] = return_list[1]
			mean_values[j] = return_list[0]
		plot.title("No of folds : %d" % i)
		plot.errorbar(range(1,6),mean_values.values(),xerr=0,yerr=std_values.values())
		plot.xlabel('K-value')
		plot.ylabel('Mean Accuracy')
		plot.ylim([20,100])
		plot.xlim([0,6])
		plot.show()
		mean_values.clear()
		std_values.clear()
main()
