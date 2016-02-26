from gensim import corpora, models, similarities
from pprint import pprint
import json
import logging
from collections import defaultdict
import subprocess
import re

def main():
	# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	t=open('../TED_dataset/newted.json')
	talks=json.loads(t.read())
	i=1;
	documents=[]
	for j in talks:
		if (i == 10):
			break
		else:
			# print "Tag corpus size: "+ str(len(tag_corpus))
			documents.append(' '.join(j['title']) ) #+ j['transcript']
			i=i+1
	# print documents[0]
	command = './run_analyzer ' + re.sub('\s\s', ' ','\"'+ str(documents[0])) +' \"' + " " +'\"'+ re.sub("\s\s", " ", str(documents[1]))+'\"'
	print "command loaded:"
	print command
	print "Finding output"
	output = subprocess.check_output(command, shell=True)
	# print output

main()