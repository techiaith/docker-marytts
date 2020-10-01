#!/usr/bin/python3
import os
import collections
import bangor_dict_utils

from shutil import copyfile

lexicon_file_path = os.path.join(os.environ['MARYTTS_CY_HOME'], 'lib/modules/cy/lexicon/geiriadur-ynganu-bangor/bangordict.dict')

valid_graphemes = bangor_dict_utils.get_graphemes(lexicon_file_path)
valid_graphemes_upper = set([x.upper() for x in valid_graphemes])

prompt_count = 0
unreliable_count = 0
ignored_count = 0
missing_graphemes = []
lexicon = set()


def writePromptFile(target_wav_filepath, prompt):
	with open (target_wav_filepath.replace('.wav','.txt'), 'w', encoding='utf-8') as text_file:
		text_file.write(prompt)


def cleanLine(line):
	line = line.rstrip()
	line = line.replace('\uFEFF','')
	line = line.replace(';','')
	line = line.replace(',','')
	line = line.replace('.','')
	line = line.replace('(','')
	line = line.replace(')','')
	line = line.replace(":",'')
	return line


def cleanPrompt(prompt):
	tokens_array = prompt.split(' ')
	for i, t in enumerate(tokens_array):
		if len(t) == 0:
			continue
		if not t[0].isalpha():
			t = t[1:]
		elif not t[-1].isalpha():
			t = t[:-1]
		
		tokens_array[i]=t

	prompt = ' '.join(tokens_array)
	return prompt


def isReliable(text):
	global prompt_count
	global unreliable_count

	prompt_count += 1
	words = set(text.split())
	lexicon.update(words)
	diff = words - valid_graphemes_upper
	if len(diff) > 0:
		#print ("WARNING: %s is not in bangor dict" % diff)
		unreliable_count += 1
		for d in diff:
			missing_graphemes.append(d)
		return False

	return True
 


def ProcessBasic(in_file, source_wavfile_dir, target_wavfile_dir):
	global ignored_count
	basic_ignored_count = 0

	ignored_file_path = os.path.join(target_wavfile_dir, "BASIC_ignored.txt")
	ignored_file = open(ignored_file_path, 'w')
	transcript_file = open(in_file,'r')

	for line in transcript_file:
		line = cleanLine(line)

		if len(line) > 0:

			orig_id, prompt = line.split('\t')
			prompt = cleanPrompt(prompt)

			if any(char.isdigit() for char in prompt):
				ignored_count += 1
				basic_ignored_count += 1
				ignored_file.write("%s %s\n" % (new_id, line))
				print ("IGNORED: ", orig_id, prompt)
			else:
				new_id = int(orig_id) + 1
				prompt = prompt.upper()
				isReliable(prompt)

				source_wav_filepath = os.path.join(source_wavfile_dir,"BASIC_%s.wav" % orig_id)
				target_wav_filepath = os.path.join(target_wavfile_dir,"sample%s.wav" % new_id)
				writePromptFile(target_wav_filepath, prompt)

				copyfile(source_wav_filepath, target_wav_filepath) 

	if basic_ignored_count > 0:
		print ("Ignored prompts logged in %s" % ignored_file_path)

	return new_id


def Processllj(in_file, start_id, source_wavfile_dir, target_wavfile_dir):
	global ignored_count
	llj_ignored_count = 0

	transcript_file = open(in_file, 'r')
	ignored_file_path = os.path.join(target_wavfile_dir, "llj_ignored.txt")
	ignored_file = open(ignored_file_path, 'w')

	orig_id = 0
	new_id = start_id

	for line in transcript_file:
		
		line = cleanLine(line)

		if len(line) > 0:
			line = cleanPrompt(line)
			if any(char.isdigit() for char in line):
				ignored_count += 1
				llj_ignored_count += 1
				ignored_file.write("%s %s\n" % (new_id, line))
				print ("IGNORED: ", new_id, line)
			else:
				prompt = line.upper()
				isReliable(prompt)
			
				src_wav_filename = 'llj_ed_%03d.wav' % (orig_id,)
				src_wav_filepath = os.path.join(source_wavfile_dir, src_wav_filename)
				trgt_wav_filepath = os.path.join(target_wavfile_dir, "sample%s.wav" % new_id)

				writePromptFile(trgt_wav_filepath, prompt)
				copyfile(src_wav_filepath, trgt_wav_filepath)
				new_id += 1

			orig_id += 1 

	if llj_ignored_count > 0:
		print ("Ignored sentences logged in %s" % ignored_file_path)

	
def main():

	if not os.path.exists("/voices/wispr/data"):
		os.makedirs("/voices/wispr/data")

	last_id = ProcessBasic('/data/Corpws-WISPR/basic/basic-000-264.txt', '/data/Corpws-WISPR/basic/wav', '/voices/wispr/data')
	Processllj('/data/Corpws-WISPR/llj/llj.txt', last_id + 1, '/data/Corpws-WISPR/llj/wav', '/voices/wispr/data')

	missing_graphemes_counts = collections.Counter(missing_graphemes)
	with open ("/voices/wispr/missing_from_dict.txt", 'w', encoding='utf-8') as missing_graphemes_file:
		for k,v in missing_graphemes_counts.most_common():
			missing_graphemes_file.write("{} {}\n".format(k,v))

	with open("/voices/wispr/lexicon.lex", 'w', encoding='utf-8') as lexicon_file:
		for w in sorted(lexicon):
			lexicon_file.write(w + "\n")

	print ("Accepted %s (although %s unreliable) prompts. Ignored %s prompts." % (prompt_count, unreliable_count, ignored_count))
	print ("%s missing graphemes written to missing_from_dict.txt" % (len(missing_graphemes_counts)))

if __name__ == "__main__":
	main()
	