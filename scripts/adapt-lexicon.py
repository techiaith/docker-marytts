#!/bin/python

import sys

f = sys.stdin

for lexicon_entry in f.read().decode('UTF-8').strip().split('\n'):
	split_entry = lexicon_entry.split(' ')

	headword = split_entry[0]
	phones = str.join(' ', split_entry[1:])

	print ("{0}|{1}".format(headword.lower().encode('UTF-8'), phones.encode('UTF-8')))

