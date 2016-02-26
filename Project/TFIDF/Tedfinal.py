import math
import json
import scipy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from itertools import izip

def sort_coo(m):
    tuples = izip(m.row, m.col, m.data)
    return sorted(tuples, key=lambda x: (x[0], x[2]), reverse=True)

def main():
	t=open('TED_dataset/ted_talks-10-Sep-2012.json')
	talks=json.loads(t.read())
	i=1;
	transcript_corpus=[]
	desc_corpus=[]
	related_vids=[]
	tdfused=[]
	for j in talks:
		if (i == 20):
			break
		else:
			transcript_corpus.append(j['transcript'])
			desc_corpus.append(j['description'])
			related_vids.append(j['related_videos'])
			i=i+1
	#print "Transcript:"
	tfidf(transcript_corpus)

def tfidf(transcript_corpus):
	vec=TfidfVectorizer(analyzer='word', ngram_range=(1,1),max_df=1.0, min_df=0.0,stop_words='english')
	tfidf=vec.fit_transform(transcript_corpus)
	print tfidf
	#cosine_similarity(tfidf)
	#pairwise_similarity = tfidf * tfidf.T
	##print pairwise_similarity.toarray()
	#x = cosine_similarity(tfidf, tfidf)



def cosine_similarity(svm):
	pairwise_similarity = svm * svm.T
	##print pairwise_similarity.toarray()
	top_k(pairwise_similarity)
	##print pairwise_similarity
	##print pairwise_similarity.shape[0]
	##print len(pairwise_similarity)

def top_k(distmatrix):
	cx = scipy.sparse.coo_matrix(distmatrix)
	cy = sort_coo(cx)
	temp = 0
	prev = -9999
	top3Indices = {}
	indicesList = []
	for i,j,v in cy:
		if i == prev or prev == -9999:
			temp += 1
			prev = i
			indicesList.append(j)
			if temp == 4:
				top3Indices[i] = indicesList
				indicesList = []
				prev = i - 1
				temp = 0
	relationDic = {}
	globalDic = {}
	Accuracy = {}
	with open("TED_dataset/ted_talks-10-Sep-2012.json","rb") as f:
		globalDic = json.load(f)	
	with open("ted_talks_relation.json", "rb") as f:
		relationDic = json.load(f)
	for key in top3Indices.keys():
		actualList = []
		for i in globalDic[key]["related_videos"]:
			##print i
			try:
				actualList.append(relationDic[i.decode('utf-8')])
			except:
				pass
		#print actualList, 
		#print top3Indices[key][1:],
		#print "==========================="
		avg=0.0
		Accuracy[key] = accuracy(top3Indices[key][1:], actualList)
	for key in Accuracy:
		avg=Accuracy[key]+avg
		# print key, Accuracy[key]
	print avg/len(Accuracy)

def accuracy(matchlist1, matchlist2):
	# print (len(list(set(matchlist1).intersection(set(matchlist2)))))
	return (((len(list(set(matchlist1).intersection(set(matchlist2))))+0.0)/3.0)) * 100
if __name__ == "__main__":
	main()
