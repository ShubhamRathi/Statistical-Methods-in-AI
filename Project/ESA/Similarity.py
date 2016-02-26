import json, itertools

def accuracy(matchlist1, matchlist2):
	# print (len(list(set(matchlist1).intersection(set(matchlist2)))))
	return (((len(list(set(matchlist1).intersection(set(matchlist2))))+0.0)/3.0)) * 100

dic={}
with open("myresults-new.json","rb") as f:
    dic = json.load(f) # LSI Predictions Dic

globalDic=[]
with open("../TED_dataset/newted.json","rb") as f:
	globalDic = json.load(f)

relationDic={}
with open("../ted_talks_relation.json", "rb") as f:
    relationDic = json.load(f)

talks = []

for talk in globalDic:
	a=[]
	for v in talk['related_videos']:
		a.append(relationDic[v])
	talks.append(a) # Ted Recommendations

l=[]
for key, value in dic.iteritems():
	l.append(value)

mean=[]
for i,j in itertools.izip(talks,l):
	print i,j
	mean.append(accuracy(i,j))
print (sum(mean)/len(mean))*100