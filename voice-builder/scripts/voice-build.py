#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import re
import sys
import subprocess
import shlex
import getopt
import logging

from shutil import copyfile

marytts_home = os.environ['MARYTTS_HOME']
marytts_version = os.environ['MARYTTS_VERSION']
marytts_builder_base = os.path.join(marytts_home, 'target', 'marytts-builder-' + marytts_version)

voices_builder_base = os.path.join(marytts_home,'voice-builder')
voices_home = os.environ['MARYTTS_VOICES_HOME']


logging.getLogger().setLevel(logging.INFO)

def get_silence_file(samplerate):
       
    silence_file = os.path.join(voices_builder_base, "silence_%skHz.wav" % samplerate)
    
    if not os.path.isfile(silence_file):
       cmd = "sox -n -r %s -b 16 -c 1 %s trim 0.0 2.0" % (samplerate, silence_file,)
       subprocess.Popen(shlex.split(cmd)).wait()

    return silence_file


def is_valid_wav(wavfile):
    if not wavfile.endswith(".wav"):
        return False

    try:
        sox_output = subprocess.check_output(["sox", wavfile, "-n", "stat"], stderr=subprocess.STDOUT).decode('utf-8')
        if 'WARN' in sox_output:
            return False
    except:
        return False

    return True


def is_silent(wavfile):

    # Typical sox output.... (not necessarily of a silent file)   
    # Samples read:             57920
    # Length (seconds):      3.620000
    # Scaled by:         2147483647.0
    # Maximum amplitude:     0.555573
    # Minimum amplitude:    -0.720520
    # Midline amplitude:    -0.082474
    # Mean    norm:          0.029584
    # Mean    amplitude:     0.000014
    # RMS     amplitude:     0.074104
    # Maximum delta:         0.677338
    # Minimum delta:         0.000000
    # Mean    delta:         0.005242
    # RMS     delta:         0.013970
    # Rough   frequency:          480
    # Volume adjustment:        1.388

    try: 
        sox_output = subprocess.check_output(["sox", wavfile, "-n", "stat"], stderr=subprocess.STDOUT).decode('utf-8')
        for attribute in sox_output.split('\n'):
            attribute = re.sub(' +', ' ', attribute)
            if attribute.startswith("Mean amplitude:"):
                mean_amplitude = float(attribute.split(':')[1].strip())
                if mean_amplitude < 0.000002 and mean_amplitude > 0.0:
                    return True
            if attribute.startswith("Maximum amplitude:"):
                max_volume = float(attribute.split(':')[1].strip())
                if max_volume < 0.0001:
                    return True

        return False

    except:
        return True


def pad_with_silence(wavfile):
    file_details = str(subprocess.check_output(["file", wavfile]))
    if '48000 Hz' in file_details: 
        silence_file = get_silence_file('48000')
        tmpwavfile = wavfile.replace(".wav","_tmp.wav")
        os.rename(wavfile, tmpwavfile)

        cmd = "sox %s %s %s %s" % (silence_file, tmpwavfile, silence_file, wavfile)
        subprocess.Popen(shlex.split(cmd)).wait()
        os.remove(tmpwavfile)   
    
    return True


def execute_java_cmd(cmd):
    try:
        logging.info(cmd)
        cmd_output = subprocess.check_output(shlex.split(cmd)).decode('utf-8')
    except:
        raise

    if 'Exception' in cmd_output:
        return False 

    return True


def init_voice_build(source_dir, voice_name):

    logging.info("init_voice_build %s started" % voice_name)

    txt_done_data = {}

    voice_build_dir = os.path.join(voices_home, voice_name)
    voice_build_recordings_dir = os.path.join(voice_build_dir, 'recordings')

    if not os.path.exists(voice_build_dir):
        os.makedirs(voice_build_dir)

    if not os.path.exists(voice_build_recordings_dir):
        os.makedirs(voice_build_recordings_dir)

    for file in os.listdir(source_dir):
        if file.endswith(".wav"):
            wavfile = os.path.join(source_dir, file)
            txtfile = wavfile.replace(".wav",".txt")
            if os.path.isfile(txtfile):
                if is_valid_wav(wavfile):
                    if not is_silent(wavfile):
                        wavfile_dest = os.path.join(voice_build_recordings_dir, file)
                        copyfile(wavfile, wavfile_dest)
                        pad_with_silence(wavfile_dest)
                        key=file.replace('.txt','')

                        with open(txtfile, 'r', encoding='utf-8') as f:
                            value=f.read()
                            txt_done_data[key]=value

    
    with open(os.path.join(voice_build_recordings_dir, 'txt.done.data'), 'w', encoding='utf-8') as txtdone:
	    for key,value in txt_done_data.items():
		    txtdone.write("( " + key + " \"" + value + "\" )\n")


    logging.info("init_voice_build %s copying templates.." % voice_name)

    # importMain.config
    copyfile(os.path.join(voices_builder_base ,'templates', 'importMain.config.template'), os.path.join(voice_build_dir,'importMain.config'))
    
    # database.config
    with open(os.path.join(voices_builder_base, 'templates', 'database.config.template'), 'r', encoding='utf-8') as src:
        lines = src.readlines()

    with open(os.path.join(voice_build_dir, 'database.config'), 'w', encoding='utf-8') as trgt:
        for line in lines:
            line = line.replace('VOICENAME', voice_name)
            line = line.replace('/home/marytts', marytts_home)
            trgt.write(line)

    logging.info("init_voice_build %s completed" % voice_name)


def audio_converter(voice_name):

    logging.info("audio converter %s starting" % voice_name)

    voice_build_dir = os.path.join(voices_home, voice_name)
    
    cmd = 'java -showversion -Xmx1024m -cp "%s/lib/*" -Dmary.base="%s" marytts.util.data.audio.AudioConverterHeadless %s' % (marytts_builder_base, marytts_builder_base, voice_build_dir,)
    return execute_java_cmd(cmd)


def voice_import(voice_name):

    logging.info("voice import starting %s" % voice_name)

    voice_build_dir = os.path.join(voices_home, voice_name)

    cmd = 'java -showversion -Xmx1024m -Dmary.base="%s" -cp "%s/lib/*" marytts.tools.voiceimport.DatabaseImportMainHeadless %s' % (marytts_builder_base, marytts_builder_base, voice_build_dir,)
    
    return execute_java_cmd(cmd)


#def voice_install(uid):
#
#    logger.info("Initiating installing voice in MaryTTS runtime API")
#
#    contents = urlopen("http://marytts-api:8008/install?voice=%s" % uid) 
#
#    logger.info("Voice installed")


def generate_voice(source_dir, voice_name):
    success = False
    try:
        init_voice_build(source_dir, voice_name)
        if audio_converter(voice_name):
            if voice_import(voice_name):
                #voice_install(voice_name)
                success = True
    except:
        logging.error("Unexpected exception: %s", sys.exc_info()[0])

    return success


def display_help():
    print ("python3 voice-build.py -v <voice name> -s <source>")


def main(argv):

    try:
        opts, args = getopt.getopt(argv,"hv:s:", ["voice=","source="])
    except getopt.GetoptError:
        display_help()
        return

    if len(opts) < 2:
        display_help()
        return

    source_audio_dir, voice_name = '',''
    for opt, arg in opts:
        if opt == '-h':
            display_help()
        elif opt in ("-v","--voice"):
            voice_name = arg
        elif opt in ("-s","--source"):
            source_audio_dir = arg

    if len(source_audio_dir) > 0 and len(voice_name) > 0:        
        generate_voice(source_audio_dir, voice_name)
    else:
        display_help()


if __name__ == "__main__":
    
    main(sys.argv[1:])
