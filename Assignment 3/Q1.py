# Example of Naive Bayes implemented from Scratch in Python
import csv
import random
import math

def loadCsv(filename):
	lines = csv.reader(open(filename, "rb"))
	dataset = list(lines)
	return dataset[1:]

def splitDataset(dataset, splitRatio):
	trainSize = int(len(dataset) * splitRatio)
	trainSet = []
	copy = list(dataset)
	while len(trainSet) < trainSize:
		index = random.randrange(len(copy))
		trainSet.append(copy.pop(index))
	return [trainSet, copy]

def separateByClass(dataset):
	separated = {}
	for i in range(len(dataset)):
		vector = dataset[i]
		if (vector[-1] not in separated):
			separated[vector[-1]] = []
		separated[vector[-1]].append(vector)
	return separated

def mean(numbers):
	return sum(numbers)/float(len(numbers))

def stdev(numbers):
	new = [int(k) for k in numbers]
	avg = mean(new)
	variance = sum([pow(float(x)-avg,2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(variance)

def summarize(dataset,discretes):
	summaries = []
	i = 0
	for attribute in zip(*dataset):
		if i not in discretes:
			new = [float(k) for k in attribute]
			summaries.append((mean(new), stdev(new)))
		else:
			a = {}
			for j in attribute:
				if j not in a:
					a[j] = 0
				a[j]+=1
			summaries.append((a,len(dataset)))
		i+=1
	del summaries[-1]
	return summaries

def summarizeByClass(dataset,discretes):
	separated = separateByClass(dataset)
	summaries = {}
	for classValue, instances in separated.iteritems():
		summaries[classValue] = {'0':summarize(instances,discretes),'1':len(instances)/float(len(dataset))}
	return summaries

def calculateProbability(x, mean, stdev):
	exponent = math.exp(-(math.pow(float(x)-mean,2)/(2*math.pow(stdev,2))))
	return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent

def calculateClassProbabilities(summaries, inputVector,discretes):
	probabilities = {}
	for classValue, classSummaries in summaries.iteritems():
		probabilities[classValue] = 0
		for i in range(len(classSummaries['0'])):
			if i not in discretes:
				"""
				mean, stdev = classSummaries[i]
				x = inputVector[i]
				print calculateProbability(x,mean,stdev)
				try:
					probabilities[classValue] += math.log(calculateProbability(x, mean, stdev))
				except:
					pass
				"""
			else:
				x = inputVector[i]
				print classValue, classSummaries['0'][i][0], classSummaries['0'][i][1]
				if x in classSummaries['0'][i][0]:
					try:
						probabilities[classValue] += math.log(classSummaries['0'][i][0][x]/float(classSummaries['0'][i][1]))
					except:
						pass
		probabilities[classValue] += math.log(classSummaries['1'])
	return probabilities
			
def predict(summaries, inputVector,discretes):
	probabilities = calculateClassProbabilities(summaries, inputVector,discretes)
	bestLabel, bestProb = None, -1
	for classValue, probability in probabilities.iteritems():
		if bestLabel is None or probability > bestProb:
			bestProb = probability
			bestLabel = classValue
	return bestLabel

def getPredictions(summaries, testSet,discretes):
	predictions = []
	for i in range(len(testSet)):
		result = predict(summaries, testSet[i],discretes)
		predictions.append(result)
	return predictions

def getAccuracy(testSet, predictions):
	correct = 0
	for i in range(len(testSet)):
		if testSet[i][-1] == predictions[i]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

def main():
	filename = 'bank-full.csv'
	discretes = [1,2,3,4,6,7,8,10,12,13,14,15,16]
	splitRatio = 0.5
	dataset = loadCsv(filename)
	trainingSet, testSet = splitDataset(dataset, splitRatio)
	print('Split {0} rows into train={1} and test={2} rows').format(len(dataset), len(trainingSet), len(testSet))
	# prepare model
	summaries = summarizeByClass(trainingSet,discretes)
	# test model
	predictions = getPredictions(summaries, testSet,discretes)
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: {0}%').format(accuracy)

main()
