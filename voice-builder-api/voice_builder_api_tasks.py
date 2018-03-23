import os
import sys
import subprocess
import codecs
import shlex

import mysql.connector

from shutil import copyfile
from celery import Celery

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


#
mysql_connection_cy = {
    'user':'root',
    'password':'commonvoice123',
    'host':'lleisiwr_mysql',
    'database':'lleisiwrvoiceweb',
}


mysql_connection_en = {
    'user':'root',
    'password':'commonvoice123',
    'host':'lleisiwr_mysql',
    'database':'lleisiwrvoiceweb_en',
}


app = Celery('voice_builder_api_tasks', broker='pyamqp://guest@localhost//')

@app.task
def generate_voice(uid):

    try:
        init_voice_build(uid)
        audio_converter(uid)
        voice_import(uid)
    except:
        logger.info("Unexpected exception: ", sys.exc_info()[0])
        return False 

    return True


def get_silence_file(samplerate):
   
    marytts_home = os.environ['MARYTTS_HOME']
    voice_build_base = os.path.join(marytts_home, 'voice-builder')
    silence_file = os.path.join(voice_build_base, "silence_%skHz.wav" % samplerate)
    
    if not os.path.isfile(silence_file):
       cmd = "sox -n -r %s -b 16 -c 1 %s trim 0.0 2.0" % (samplerate, silence_file,)
       subprocess.Popen(shlex.split(cmd)).wait()

    return silence_file


def is_valid_wav(wavfile):
    if not wavfile.endswith(".wav"):
        return False;

    marytts_home = os.environ['MARYTTS_HOME']
    voice_build_base = os.path.join(marytts_home, 'voice-builder')
    sox_output = subprocess.check_output(["sox", wavfile, "-n", "stat"], stderr=subprocess.STDOUT).decode('utf-8')

    if 'WARN' in sox_output:
        return False

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


def init_voice_build(uid):

    logger.info("init_voice_build %s started" % uid)

    txt_done_data = {}
    voice_name = uid

    marytts_home = os.environ['MARYTTS_HOME']
    marytts_version = os.environ['MARYTTS_VERSION']

    marytts_base = os.path.join(marytts_home, 'target', 'marytts-builder-' + marytts_version)
    voice_build_dir = os.path.join(marytts_home, 'voice-builder', uid)
    commonvoice_recordings_dir = os.path.join('/commonvoice-recordings', uid)
    voice_build_recordings_dir = os.path.join(voice_build_dir, 'recordings')

    if not os.path.exists(voice_build_dir):
        os.makedirs(voice_build_dir)

    if not os.path.exists(voice_build_recordings_dir):
        os.makedirs(voice_build_recordings_dir)

    # fetch list of recordings for uid from database
    cnx = mysql.connector.connect(**mysql_connection_cy)
    cursor = cnx.cursor()
    query = "SELECT s.guid FROM Sentences s WHERE s.guid IN (SELECT rs.guid FROM RecordedSentences rs WHERE rs.uid=%s)"
    cursor.execute(query, (uid,))
    for row in cursor:
        guid = row[0]
        txtfile = os.path.join(commonvoice_recordings_dir, guid + '.txt')
        wavfile = os.path.join(commonvoice_recordings_dir, guid + '.wav')
        if is_valid_wav(wavfile): 
            wavfile_dest = os.path.join(voice_build_recordings_dir, guid + '.wav')
            copyfile(wavfile, wavfile_dest)
            pad_with_silence(wavfile_dest) 
            with codecs.open(txtfile, 'r', encoding='utf-8') as t:
                text = t.read()
                txt_done_data[guid]=text

    cursor.close()
    cnx.close()

    # txt.done.data
    with codecs.open(os.path.join(voice_build_dir, 'txt.done.data'), 'w', encoding='utf-8') as txtdone:
        for key,value in txt_done_data.items():
                txtdone.write("( " + key + " \"" + value + "\" )\n")

    # importMain.config
    copyfile(os.path.join(marytts_home, 'voice-builder', 'recorder', 'importMain.config.template'), os.path.join(voice_build_dir,'importMain.config'))
    
    # database.config
    with open(os.path.join(marytts_home, 'voice-builder', 'recorder', 'database.config.template'), 'r', encoding='utf-8') as src:
        lines = src.readlines()

    with open(os.path.join(voice_build_dir, 'database.config'), 'w', encoding='utf-8') as trgt:
        for line in lines:
            line = line.replace('VOICENAME', voice_name)
            line = line.replace('/home/marytts', marytts_home)
            trgt.write(line)

    logger.info("init_voice_build %s completed" % uid)



def audio_converter(uid):

    logger.info("audio converter %s starting" % uid)

    marytts_home = os.environ['MARYTTS_HOME']
    marytts_version = os.environ['MARYTTS_VERSION']

    marytts_base = os.path.join(marytts_home, 'target', 'marytts-builder-' + marytts_version)
    voice_build_dir = os.path.join(marytts_home, 'voice-builder/', uid)

    cmd = 'java -showversion -Xmx1024m -cp "%s/lib/*" -Dmary.base="%s" marytts.util.data.audio.AudioConverterHeadless %s' % (marytts_base, marytts_base, voice_build_dir,)
    shlex_cmd = shlex.split(cmd)

    try:
        subprocess.check_output(shlex_cmd)
    except subprocess.CalledProcessError as e:
        logger.info(e.output)
        raise
    except:
        raise

    logger.info("audio converter %s completed" % uid)



def voice_import(uid):

    logger.info("voice import starting %s" % uid)

    marytts_home = os.environ['MARYTTS_HOME']
    marytts_version = os.environ['MARYTTS_VERSION']

    marytts_base = os.path.join(marytts_home, 'target', 'marytts-builder-' + marytts_version)
    voice_build_dir = os.path.join(marytts_home, '/opt/marytts/voice-builder/', uid)

    subprocess.call(['java -showversion -Xmx1024m -Dmary.base="%s" -cp "%s/lib/*" marytts.tools.voiceimport.DatabaseImportMainHeadless %s' % (marytts_base, marytts_base, voice_build_dir,)], shell=True)
    
    logger.info("voice import completed")


