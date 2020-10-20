import os
import re
import sys

from celery import Celery
from urllib.request import urlopen

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

import voice_build

source_recordings = '/recordings'  #os.environ['SOURCE_RECORDINGS']

app = Celery('voice_builder_api_tasks', broker='pyamqp://guest@localhost//')

@app.task
def generate_voice(uid, locale):
    source_audio_dir = os.path.join(source_recordings, locale, uid)
    voice_name = '%s_%s' % (uid, locale)
    success = voice_build.generate_voice(source_audio_dir, voice_name, locale) 

    if not success:
        logger.info('Generate voice not successful')
    else:
        voice_install(voice_name)

    return success



def voice_install(voice_name):
    logger.info("Initiating installing voice in MaryTTS runtime API")
    contents = urlopen("http://marytts-api:8008/install?voice=%s" % voice_name) 
    logger.info("Voice installed")

