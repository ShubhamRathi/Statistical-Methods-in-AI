from gensim import corpora, models, similarities
from pprint import pprint
import json
import logging
from collections import defaultdict
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def main():
	# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	t=open('../TED_dataset/newted.json')
	talks=json.loads(t.read())
	i=1;
	documents=[]
	test=[]
	for j in talks:
		if (i > 10000):
			break
		else:
			# print "Tag corpus size: "+ str(len(tag_corpus))
			documents.append(j['description'][0] ) #+ j['transcript']
			i=i+1
	# remove common words and tokenize
	stoplist = set('for a of the and to in'.split())
	texts = [[word for word in document.lower().split() if word not in stoplist]for document in documents]

	# remove words that appear only once	
	frequency = defaultdict(int)
	for text in texts:
		for token in text:
			frequency[token] += 1
	texts = [[token for token in text if frequency[token] > 1] for text in texts]
	#pprint(texts) # Pretty Print
	#print len(texts)
	dictionary = corpora.Dictionary(texts)
	# print dictionary
	# print dictionary
	# print(dictionary.token2id)
	corpus = [dictionary.doc2bow(text) for text in texts]
	# print corpus
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	# print corpus_tfidf
	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)
	corpus_lsi = lsi[corpus_tfidf]	
	# write out coordinates to file
	fcoords = open(os.path.join("./Coordinates", "tfidf.csv"), 'wb')
	for vector in tfidf[corpus]:
		fcoords.write("%6.4f\t%6.4f\n" % (vector[0][1], vector[1][1]))
		# print vector
	fcoords.close()

	MODELS_DIR = "Coordinates/"
	MAX_K = 400
	X = np.loadtxt(os.path.join(MODELS_DIR, "tfidf.csv"), delimiter="\t")
	ks = range(1, MAX_K + 1)
	inertias = np.zeros(MAX_K)
	diff = np.zeros(MAX_K)
	diff2 = np.zeros(MAX_K)
	diff3 = np.zeros(MAX_K)
	for k in ks:
		kmeans = KMeans(k).fit(X)
		inertias[k - 1] = kmeans.inertia_
		# first difference
		if k > 1:
			diff[k - 1] = inertias[k - 1] - inertias[k - 2]
		# second difference
		if k > 2:
			diff2[k - 1] = diff[k - 1] - diff[k - 2]
		# third difference
		if k > 3:
			diff3[k - 1] = diff2[k - 1] - diff2[k - 2]
	elbow = np.argmin(diff3[3:]) + 3
	plt.plot(ks, inertias, "b*-")
	plt.plot(ks[elbow], inertias[elbow], marker='o', markersize=12,markeredgewidth=2, markeredgecolor='r', markerfacecolor=None)
	plt.ylabel("Inertia")
	plt.xlabel("K")
	plt.show()


main()