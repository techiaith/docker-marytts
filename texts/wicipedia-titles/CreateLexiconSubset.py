#!/usr/bin/env python3

#
# Copyright 2017 Prifysgol Bangor University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys, os, subprocess, string
import urllib.request
import cld2
import spacy
import csv

nlp=spacy.load('en') # use only the tokenizer. 

cy_pron_lex=[]
cylexicon, header = urllib.request.urlretrieve("http://techiaith.cymru/lts/cym.lexicon")
cylexicon_file = open(cylexicon,'r')
for p in cylexicon_file:
	l=p.split(' ')[0]
	d=nlp(l)
	for t in d:
		if t.text in string.punctuation:
			continue
		cy_pron_lex.append(t.text)

cy = []
cy_cld2 = []
xx = []
		
cy_file = open('lexicon.cy','w')
cy_cld2_file = open('lexicon_cld2.cy','w')
xx_file = open('lexicon.xx','w')

def add_to_lexicon_file(text):
	tokens=nlp(text.rstrip())
	for t in tokens:
		token=t.text.rstrip()
		if token.endswith("'r") or token.endswith("'n"):
			token=token.split("'")[0]

		if token in string.punctuation:
			continue

		if token in cy_pron_lex:
			cy.append(token)
			continue 
		

		isReliable, textBytesFound, details = cld2.detect(token)
		langcode=details[0][1]
		if langcode=='cy':
			cy_cld2.append(token)	
		else:
			xx.append(token)

	
def uniq_and_sorted_to_file(alist, outfile):
	aset=set(alist)
	alist_uniq=list(aset)
	alist_uniq_sorted=sorted(alist_uniq)
	for item in alist_uniq_sorted:
		outfile.write(item + "\n")		


def main():
	with open('Wicipedia-Titles.csv','r') as titles:
		reader = csv.DictReader(titles, delimiter='\t')
		for row in reader:
			try:
				title=row['title']
				print (title)
				title=title.replace("_"," ")
				title=title.rstrip().upper()
				add_to_lexicon_file(title)	
			except KeyboardInterrupt:
				sys.exit(1)	
			except:
				print ("EXCEPTION: " + title)
				print (sys.exc_info())


	uniq_and_sorted_to_file(cy, cy_file)
	uniq_and_sorted_to_file(cy_cld2, cy_cld2_file)
	uniq_and_sorted_to_file(xx, xx_file)

	cy_file.close()
	cy_cld2_file.close()
	xx_file.close()


if __name__ == "__main__":
	main()

