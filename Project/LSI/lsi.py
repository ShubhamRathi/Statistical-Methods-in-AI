from gensim import corpora, models, similarities
from pprint import pprint
import json
import logging
from collections import defaultdict

def main():
	# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	t=open('../TED_dataset/newted.json')
	talks=json.loads(t.read())
	i=1;
	documents=[]
	for j in talks:
		if (i == 1000000):
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
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	# print corpus_tfidf
	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)
	corpus_lsi = lsi[corpus_tfidf]		
	counter=0
	dic = {}
	for doc in documents:
		vec_bow = dictionary.doc2bow(doc.lower().split())		
		vec_lsi = lsi[vec_bow]
		# index = similarities.MatrixSimilarity(lsi[corpus])
		# sims = index[vec_lsi]
		# sims = sorted(enumerate(sims), key=lambda item: -item[1])
		# print sims
		# dic[counter] = [ x[0] for x in sims[1:4]]
		# counter=counter+1
	# with open("myresults.json","wb") as f:
	# 	json.dump(dic, f)
main()



