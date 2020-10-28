############################
#
#  Changes the speaker of the sounds 
#  in a specificed directory with preset parameters. 
#  Files are saved in a specified directory.
#  s.cooper@bangor.ac.uk 
#
############################


form Change speaker in directory 
	## Directory of sound files
	text sound_directory /home/techiaith/src/docker-marytts/recordings/dafydd-tts-cy/
	sentence Sound_file_extension .wav
	## Directory of finished files
	text end_directory /home/techiaith/src/docker-marytts/recordings/dafydd-tts-cy-praat/

endform

# Here, we list all of the sound files in the directory.

Create Strings as file list... list 'sound_directory$'*'sound_file_extension$'
numberOfFiles = Get number of strings


for ifile to numberOfFiles
	filename$ = Get string... ifile

	# Open files from the list outlined above:

	sound_one = Read from file... 'sound_directory$''filename$'
#	sound_one = selected$ ("Sound")


	# Perform change speaker:
	# Remember settings for Change speaker are complicated
	# Change speaker parameters = pitch floor, pitch ceiling, multiply formants by, multiply pitch by, multiply range by, multiply duration b
	# Read info here: http://www.fon.hum.uva.nl/praat/manual/Sound__Change_speaker___.html
	# And here: https://uk.groups.yahoo.com/neo/groups/praat-users/conversations/topics/1397?guccounter=1
	# Keep multiply formants by between 0.8 and 1.5 to prevent Mickey Mouse effetcs
	# The accuracy of the change speaker depends on the pitch analysis so first two numbers are important
	# These settings are to change older man to sound like younger man, also difference in speech rate
	
	sound_two = Change speaker... 75 400 1.09 1.12 1.508 0.9
	
	# Also option of Change gender... which works for age too. Unclear what difference between Change gender and Change speaker is, but Change gender allows new pitch median where Change speaker does not. 
	# Change gender parameters: pitch floor, pitch ceiling, Formant shift ratio, new pitch median, pitch range factor, duration factor
	# sound_two = Change speaker... 75 400 1.09 1.12 1 0.9
	# This doesn't really work. Commented out for future experiments. 

	# Save the resulting file:

	select 'sound_two'
		Write to WAV file... 'end_directory$''filename$'

	 
	Remove

	select Strings list
endfor

select all
Remove
	
