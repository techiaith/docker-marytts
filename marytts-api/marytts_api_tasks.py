import os
import codecs

import mysql.connector

from shutil import copyfile
from celery import Celery
from subprocess import call

mysql_connection = {
    'user':'root',
    'password':'commonvoice123',
    'host':'lleisiwr_mysql',
    'database':'lleisiwrvoiceweb',
}

app = Celery('marytts_api_tasks', broker='pyamqp://guest@localhost//')

@app.task
def generate_voice(uid):

    init_voice_build(uid)

    audio_converter(uid)


    ###BINDIR="`dirname "$0"`"
    ###export MARY_BASE="`(cd "$BINDIR"/.. ; pwd)`"
    ###java -showversion -Xmx1024m -Dmary.base="$MARY_BASE" -cp "$MARY_BASE/lib/*" marytts.tools.voiceimport.DatabaseImportMainHeadless $*

    return True


def init_voice_build(uid):

    txt_done_data = {}
    voice_name = uid

    commonvoice_recordings_dir = os.path.join('/commonvoice-recordings', uid)
    voice_build_dir = os.path.join('/opt/marytts/voice-builder/', voice_name)
    voice_build_recordings_dir = os.path.join(voice_build_dir, 'recordings')

    if not os.path.exists(voice_build_dir):
        os.makedirs(voice_build_dir)

    if not os.path.exists(voice_build_recordings_dir):
        os.makedirs(voice_build_recordings_dir)

    # fetch list of recordings for uid from database
    cnx = mysql.connector.connect(**mysql_connection)
    cursor = cnx.cursor()
    query = "select guid from RecordedSentences where uid=%s"
    cursor.execute(query, (uid,))
    for row in cursor:
        guid = row[0]
        txtfile = os.path.join(commonvoice_recordings_dir, guid + '.txt')
        wavfile = os.path.join(commonvoice_recordings_dir, guid + '.wav')
        wavfile_dest = os.path.join(voice_build_recordings_dir, guid + '.wav')
        copyfile(wavfile, wavfile_dest)

        with codecs.open(txtfile, 'r', encoding='utf-8') as t:
            text = t.read()
            txt_done_data[guid]=text

    cursor.close()
    cnx.close()

    with codecs.open(os.path.join(voice_build_dir, 'txt.done.data'), 'w', encoding='utf-8') as txtdone:
        for key,value in txt_done_data.items():
                txtdone.write("( " + key + " \"" + value + "\" )\n")

    # importMain.config
    copyfile('/opt/marytts/voice-builder/recorder/importMain.config.template', os.path.join(voice_build_dir,'importMain.config'))
    
    # database.config
    with open('/opt/marytts/voice-builder/recorder/database.config.template', 'r', encoding='utf-8') as src:
        lines = src.readlines()
    with open(os.path.join(voice_build_dir, 'database.config'), 'w', encoding='utf-8') as trgt:
        for line in lines:
            line = line.replace('VOICENAME', voice_name)
            line = line.replace('/home/marytts','/opt/marytts')
            trgt.write(line.rstrip() + '\n')


def audio_converter(uid):

    # java instructions...
    ## audio_converter
    marytts_home = os.environ['MARYTTS_HOME']
    marytts_version = os.environ['MARYTTS_VERSION']

    marytts_base = os.path.join(marytts_home, 'target', 'marytts-builder-' + marytts_version)
    voice_build_dir = os.path.join('/opt/marytts/voice-builder/', uid)


    #call(['java','-showversion', '-Xmx1024m', '-Dmary.base="%s"' % (marytts_base,), '-cp "%s/lib/*"' % (marytts_base,), 'marytts.util.data.audio.AudioConverterHeadless', '%s' % (voice_build_dir,)])
    call(['java -showversion -Xmx1024m -Dmary.base="%s" -cp "%s/lib/*" marytts.util.data.audio.AudioConverterHeadless %s' % (marytts_base, marytts_base, voice_build_dir,)], shell=True)
