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
	fcoords = open(os.path.join("./Coordinates", "lda.csv"), 'wb')
	corpus = [dictionary.doc2bow(text) for text in texts]
	lda = models.ldamodel.LdaModel(corpus, num_topics=100, id2word=dictionary)
	doc_topic = lda.doc_topic_
	f, ax= plt.subplots(5, 1, figsize=(8, 6), sharex=True)
	for i, k in enumerate([0, 5, 9, 14, 19]):
	    ax[i].stem(topic_word[k,:], linefmt='b-',
	               markerfmt='bo', basefmt='w-')
	    ax[i].set_xlim(-50,4350)
	    ax[i].set_ylim(0, 0.08)
	    ax[i].set_ylabel("Prob")
	    ax[i].set_title("topic {}".format(k))

	ax[4].set_xlabel("word")

	plt.tight_layout()
	plt.show()
	


main()