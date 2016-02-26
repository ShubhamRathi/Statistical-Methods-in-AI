from gensim import corpora, models, similarities
import json
from pprint import pprint
import logging
from collections import defaultdict
import subprocess
import re
import json
from operator import itemgetter

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
			documents.append(' '.join(j['description']) ) #+ j['transcript']
			i=i+1
	# print documents[0]
	points={0:[]}
	for i in range(1200):
		target = open('sim.json', 'wb')
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
		json.dump(points, target)
		# Append ans to a dict[#TalkNo]
	#print points
		target.close()

main()