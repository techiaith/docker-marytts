#!/bin/python3

import os, sys


src_dir = sys.argv[1]
txt_done_data = {}

for file in os.listdir(src_dir):
	if file.endswith(".txt"):
		key=file.replace('.txt','')
		with open(os.path.join(src_dir,file), 'r', encoding='utf-8') as f:
			value=f.read()
			txt_done_data[key]=value

with open('txt.done.data', 'w', encoding='utf-8') as txtdone:
	for key,value in txt_done_data.items():
		txtdone.write("( " + key + " \"" + value + "\" )\n")	

	
