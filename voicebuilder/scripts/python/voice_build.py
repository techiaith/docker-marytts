#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import re
import sys
import subprocess
import shlex
import getopt
import logging
import traceback

from pathlib import Path
from shutil import copyfile

marytts_home = os.environ['MARYTTS_HOME']
marytts_version = os.environ['MARYTTS_VERSION']
marytts_builder_base = os.path.join(marytts_home, 'target', 'marytts-builder-' + marytts_version)

voices_builder_base = os.path.join(marytts_home,'voicebuilder')
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


def valid_pitch_pointers(wavfile):
    if not wavfile.endswith(".wav"):
        return False

    try:
        praat_script = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pitch.praat')
        cmd = "praat --run %s %s 75 300" % (praat_script, wavfile)
        praat_output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        if len(praat_output) >0 and b'Error' in praat_output:
            return False
    except Exception:
        traceback.print_exc()
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
    except Exception as ex:
        logging.info("voice_build.py::execute_java_cmd exception " + ex)
        raise

    if 'Exception' in cmd_output:
        logging.info("voice_build.py::execute_java_cmd, 'Exception' in output: " + cmd_output)
        return False

    logging.info("voice_build.py::execute_java_cmd completed successfully")

    return True


def rename_file_extension(filepath, newextension):
    base = os.path.splitext(filepath)[0]
    os.rename(filepath, base + newextension)


def init_voice_build(voice_build_dir, voice_name, locale):

    logging.info("init_voice_build: voice_build_dir %s, voice_name %s - started" % (voice_build_dir, voice_name))

    txt_done_data = {}

    voice_wavs_dir = os.path.join(voice_build_dir, 'wav')
    voice_prompts_dir = os.path.join(voice_build_dir, 'data')

    # renaming will exclude wav files from MaryTTS basenamelist
    for file in os.listdir(voice_wavs_dir):
        if file.endswith(".wav"):
            wavfile = os.path.join(voice_wavs_dir, file)
            txtfile = os.path.join(voice_prompts_dir, file.replace(".wav",".txt"))

            if not os.path.isfile(txtfile):
                logging.info("voice_build.py couldn't find txtfile %s " % txtfile)
                rename_file_extension(wavfile, ".notextfile")
                continue

            if not is_valid_wav(wavfile):
                logging.info("voice_build.py found that %s not a valid wavfile " % wavfile)
                rename_file_extension(wavfile, ".notvalidwavfile")
                continue

            #if is_silent(wavfile):
                #logging.info("voice_build.py found that %s is silent" % wavfile)
                #rename_file_extension(wavfile, ".silentwavfile")
                #continue

            if not valid_pitch_pointers(wavfile):
                logging.info("voice_build.py found that %s has invalid pitch pointers" % wavfile)
                rename_file_extension(wavfile, ".invalidpitchpointers")
                continue

            pad_with_silence(wavfile)
            key=file.replace('.wav','')

            with open(txtfile, 'r', encoding='utf-8') as f:
                value=f.read()
                txt_done_data[key]=value.strip()


    with open(os.path.join(voice_build_dir, 'txt.done.data'), 'w', encoding='utf-8') as txtdone:
        for key,value in txt_done_data.items():
            txtdone.write("( " + key + " \"" + value + "\" )\n")

    #
    logging.info("voice_build.py::init_voice_build %s copying templates.." % voice_name)

    # importMain.config
    copyfile(os.path.join(voices_builder_base ,'templates', 'importMain.config.template'), os.path.join(voice_build_dir,'importMain.config'))

    # database.config
    with open(os.path.join(voices_builder_base, 'templates', 'database.config.template'), 'r', encoding='utf-8') as src:
        lines = src.readlines()

    with open(os.path.join(voice_build_dir, 'database.config'), 'w', encoding='utf-8') as trgt:
        for line in lines:
            line = line.replace('VOICE_BUILD_DIR', voice_build_dir)
            line = line.replace('VOICENAME', voice_name)
            line = line.replace('VOICE_LOCALE', locale)
            trgt.write(line)

    logging.info("voice_build.py::init_voice_build %s completed" % voice_name)



def audio_converter(voice_build_recordings_dir, voice_build_dir, voice_name):

    logging.info("audio_converter %s " % voice_build_dir)
    voice_build_wavs_dir = os.path.join(voice_build_dir, "wav")

    Path(voice_build_wavs_dir).mkdir(parents=True, exist_ok=True)

    #cmd = 'java -showversion -Xmx1024m -cp "%s/lib/*" -Dmary.base="%s" marytts.util.data.audio.AudioConverterHeadless %s %s' % (marytts_builder_base, marytts_builder_base, voice_build_recordings_dir, voice_build_wavs_dir)
    cmd = 'java -cp "%s/lib/*" -Dmary.base="%s" marytts.util.data.audio.AudioConverterHeadless %s %s' % (marytts_builder_base, marytts_builder_base, voice_build_recordings_dir, voice_build_wavs_dir)

    return execute_java_cmd(cmd)


def voice_import(voice_name):

    logging.info("voice_build.py::voice import starting %s" % voice_name)

    voice_build_dir = os.path.join(voices_home, voice_name)

    cmd = 'java -cp "%s/lib/*" -Dmary.base="%s" marytts.tools.voiceimport.DatabaseImportMainHeadless %s' % (marytts_builder_base, marytts_builder_base, voice_build_dir)

    return execute_java_cmd(cmd)



def generate_voice(audio_source_dir, voice_name, locale, peform_speech_analysis=False):
    logging.info("generate_voice: source_dir %s, voice_name %s, locale %s" % (audio_source_dir, voice_name, locale))
    success = False
    try:
        voice_build_dir = os.path.join(voices_home, voice_name)
        logging.info("Creating voice in dir %s" % voice_build_dir)

        if audio_converter(audio_source_dir, voice_build_dir, voice_name):
            init_voice_build(voice_build_dir, voice_name, locale)
            if voice_import(voice_name):
                logging.info("voice built successfully")
                success = True
    except:
        logging.error("Unexpected exception: %s", sys.exc_info()[0])

    return success


def display_help():
    print ("")
    print ("Build a marytts voice from the command line")
    print ("")
    print ("Usage:")
    print ("")
    print ("$ voice-build.py -v <voice name> -l <locale>")


def main(argv):

    try:
         opts, args = getopt.getopt(argv,"hv:s:l:", ["voice=","source=","locale="])
    except getopt.GetoptError:
        display_help()
        return

    if len(opts) < 2:
        display_help()
        return

    source_audio_dir, voice_name, locale = '','',''
    for opt, arg in opts:
        if opt == '-h':
            display_help()
        elif opt in ("-v","--voice"):
            voice_name = arg
        elif opt in ("-s","--source"):
            source_audio_dir = arg
        elif opt in ("-l","--locale"):
            locale = arg

    if len(source_audio_dir) > 0 and len(voice_name) > 0:
        generate_voice(source_audio_dir, voice_name, locale, False)
    else:
        display_help()


if __name__ == "__main__":

    main(sys.argv[1:])
