import csv
import random
import math
import operator

def main():
	trainingSet=[]
	testSet=[]
	filename='iris.data'
	with open(filename, 'rb') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(0,4):
	            dataset[x][y] = float(dataset[x][y])
	#print len(dataset)
	random.shuffle(dataset)
	print (dataset)

main()