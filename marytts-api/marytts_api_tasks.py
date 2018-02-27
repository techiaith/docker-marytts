import os
import time

import mysql.connector
from shutil import copyfile

from celery import Celery

mysql_connection = {
    'user':'root',
    'password':'commonvoice123',
    'host':'lleisiwr_mysql',
    'database':'lleisiwrvoiceweb',
}

app = Celery('marytts_api_tasks', broker='pyamqp://guest@localhost//')

@app.task
def generate_voice(uid):

    time.sleep(60)

    init_voice_build(uid)
    # copy files from external recordings


    # java instructions...
    ## audio_converter

    ###BINDIR="`dirname "$0"`"
    ###export MARY_BASE="`(cd "$BINDIR"/.. ; pwd)`"
    ###echo $MARY_BASE
    ###java -showversion -Xmx1024m -Dmary.base="$MARY_BASE" -cp "$MARY_BASE/lib/*" marytts.util.data.audio.AudioConverterHeadless $1

    ###BINDIR="`dirname "$0"`"
    ###export MARY_BASE="`(cd "$BINDIR"/.. ; pwd)`"
    ###java -showversion -Xmx1024m -Dmary.base="$MARY_BASE" -cp "$MARY_BASE/lib/*" marytts.tools.voiceimport.DatabaseImportMainHeadless $*

    return true

def init_voice_build(uid):

    txt_done_data = {}
    voice_name = uid

    commonvoice_recordings_dir = os.path.join('commonvoice-recordings', uid)
    voice_build_dir = os.path.join('/opt/marytts/voice-builder/', voice_name)
    voice_build_recordings_dir = os.path.join(voice_build_dir, 'recordings')

    if not os.path.exists(voice_build_dir):
        os.makedirs(voice_build_dir)

    if not os.path.exists(voice_build_recordings_dir):
        os.makedirs(voice_build_recordings_dir)

    # fetch list of recordings for uid from database
    cnx = mysql.connector.connect(**mysql_connection)
    cursor = cnx.cursor()
    query = "select sentence_id from RecordedSentences where uid='" + uid + "'"
    for (sentence_id) in cursor:
        print (sentence_id)
        copyfile(os.path.join(os.path.join(commonvoice_recordings_dir,sentence_id + '.wav'), voice_build_recordings_dir)

        with open(os.path.join(commonvoice_recordings_dir, sentence_id + '.txt', 'r', encoding='utf-8') as t:
            text = t.read()
            txt_done_data[sentence_id]=text


    with open(os.path.join(voice_build_dir, 'txt.done.data'), 'w', encoding='utf-8') as txtdone:
        for key,value in txt_done_data.items():
                txtdone.write("( " + key + " \"" + value + "\" )\n")

    # importMain.config
    copyfile('/opt/marytts/voice-builder/recorder/importMain.config.template', os.path.join(voice_build_dir,importMain.config))
    
    # database.config
    with open('/opt/marytts/voice-builder/recorder/database.config.template', 'r', encoding='utf-8') as src:
        lines = src.readlines()
    with open(os.path.join(voice_build_dir, 'database.config'), 'w', encoding='utf-8') as trgt:
        for line in lines:
            line = line.replace('VOICENAME', voice_name)
            trgt.write(line + '\n')


