from pca import *
import numpy as NP
import naive_base as nb
from lda import *
df = "arcene_train.data"
#data = NP.loadtxt(df,delimiter=" ")
data = NP.genfromtxt(df, delimiter=' ')[:,:201]
print data
def for_pca(data):
	print "enter dimension to reduced to"
	k = raw_input()
	result = plot_pca(data,int(k))
	i = 0
	class_file = open("arcene_train.labels","r")
	a = []
	for line in class_file:
		a.append(NP.append(result[i],[int(line)]))
		i+=1
	print a
	nb.naive_base(a)
	
def for_lda(data):
	class_file = open("arcene_train.labels","r")
	a = []
	i = 0
	for line in class_file:
		a.append((list(data[i]) + [int(line),]))
		i+=1
	print a
	result  = lda_main(NP.array(a))
	i = 0
	class_file.close()
	class_file = open("arcene_train.labels","r")
	a = []
	for line in class_file:
		a.append(list(result[i]) + [int(line)])
	print a
	nb.naive_base(NP.array(a))

def main():
	print "enter 1 for PCA 2 for LDA"
	x = int(raw_input())
	if x == 1:
		for_pca(data)
	else:
		for_lda(data)

main()
