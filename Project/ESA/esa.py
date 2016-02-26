from gensim import corpora, models, similarities
import json
from pprint import pprint
import logging
from collections import defaultdict
import subprocess
import re
import json
from nltk.corpus import stopwords

def main():
	# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	t=open('../TED_dataset/newted.json')
	talks=json.loads(t.read())
	i=1;
	documents=[]
	for j in talks:
		if (i == 1202):
			break
		else:
			# print "Tag corpus size: "+ str(len(tag_corpus))
			text=' '.join(j['description'])
			text=text.split (' ')
			for word in text:
				if word in stopwords.words('english'):
					text.remove(word)
					# print "Removed: ", word
			text= " ".join(text)
			documents.append(text) #+ j['transcript']
			i=i+1
	# print documents[0]
	target = open('sim.json', 'wb')
	points={0:[]}
	target.write("{")
	for i in range(10):
		# print "i is ", i
		ans=[]
		for j in range(1200):
			# print "j is ",j
			command = ['./run_analyzer'," ".join(documents[i].split())," ".join(documents[j].split())]
			# print command
			output = subprocess.Popen(command,stdout=subprocess.PIPE, shell=False)
			for line in output.stdout:
				if re.match(r'^[+-]?([0-1]+((\.{1})\d*)|(\.){1}\d+)([eE][+-]?\d*)?$',line.strip()):
					# print "Appended: ",line
					ans.append(line.strip())
					# ans[-1] = ans[-1].strip()
		points[i] = list(ans)
		output.stdout.close()
		target.write(str(i)+":"+str(points[i]))
		if i < 9:
			target.write(",")
	target.write("}")
		# Append ans to a dict[#TalkNo]
	#print points
	target.close()

main()