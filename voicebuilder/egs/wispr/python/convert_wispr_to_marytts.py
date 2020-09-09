#!/usr/bin/python3
import os
from shutil import copyfile


def writePromptFile(target_wav_filepath, prompt):
	with open (target_wav_filepath.replace('.wav','.txt'), 'w', encoding='utf-8') as text_file:
		text_file.write(prompt)

def cleanPrompt(line):

	line = line.rstrip()
	line = line.replace('\uFEFF','')
	line = line.replace(';','')
	line = line.replace(',','')
	line = line.replace('.','')

	return line

	
def ProcessBasic(in_file, source_wavfile_dir, target_wavfile_dir):

	transcript_file = open(in_file,'r')

	for line in transcript_file:

		line = cleanPrompt(line)		

		if len(line) > 0:
			orig_id, prompt = line.split('\t')

			if any(char.isdigit() for char in prompt):
				print (orig_id, prompt)
			new_id = int(orig_id) + 1
			prompt = prompt.upper()

			source_wav_filepath = os.path.join(source_wavfile_dir,"BASIC_%s.wav" % orig_id) 
			target_wav_filepath = os.path.join(target_wavfile_dir,"sample%s.wav" % new_id)
			writePromptFile(target_wav_filepath, prompt)

			copyfile(source_wav_filepath, target_wav_filepath) 


	return new_id


def Processllj(in_file, start_id, source_wavfile_dir, target_wavfile_dir):
	
	transcript_file = open(in_file, 'r')

	orig_id = 0
	new_id = start_id

	for line in transcript_file:
		
		line = cleanPrompt(line)

		if len(line) > 0:

			if any(char.isdigit() for char in line):
				print (new_id, line)
			else:

				prompt = line.upper()
			
				src_wav_filename = 'llj_ed_%03d.wav' % (orig_id,)
				src_wav_filepath = os.path.join(source_wavfile_dir, src_wav_filename)
				trgt_wav_filepath = os.path.join(target_wavfile_dir, "sample%s.wav" % new_id)

				writePromptFile(trgt_wav_filepath, prompt)
				copyfile(os.path.join(source_wavfile_dir, src_wav_filename),
					os.path.join(target_wavfile_dir, "sample%s.wav" % new_id))
				new_id += 1

			orig_id += 1 
				
	
def main():

	if not os.path.exists("/voices/wispr/recordings"):
		os.makedirs("/voices/wispr/recordings")

	last_id = ProcessBasic('/recordings/Corpws-WISPR/basic/basic-000-264.txt', '/recordings/Corpws-WISPR/basic/wav', '/voices/wispr/recordings')
	Processllj('/recordings/Corpws-WISPR/llj/llj.txt', last_id + 1, '/recordings/Corpws-WISPR/llj/wav', '/voices/wispr/recordings')


if __name__ == "__main__":
	main()
	

