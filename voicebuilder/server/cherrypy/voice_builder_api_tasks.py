import os
import re
import sys

from pathlib import Path
import shutil
from celery import Celery
from urllib.request import urlopen

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

import voice_build

source_recordings = '/recordings/lleisiwr'  #os.environ['SOURCE_RECORDINGS']

app = Celery('voice_builder_api_tasks', broker='pyamqp://guest@localhost//')

@app.task
def generate_voice(uid):
    source_audio_dir = os.path.join(source_recordings, uid)
    voice_name = '%s_cy' % (uid)

    # place recordings in suitable location for marytts voicebuild 
    if os.path.isdir(source_audio_dir):

        # copy every file over to /voices/<voice_name>/data
        voice_dir = os.path.join("/voices", voice_name)
        if os.path.exists(voice_dir):
            shutil.rmtree(voice_dir)

        #
        voice_data_dir = os.path.join(voice_dir, "data")

        Path(voice_data_dir).mkdir(parents=True, exist_ok=True)
        
        logger.info("Copying audio recordings from %s to %s" % (source_audio_dir, voice_data_dir))
        
        src_files = os.listdir(source_audio_dir)
        for filename in src_files:
            full_filepath = os.path.join(source_audio_dir, filename)
            if os.path.isfile(full_filepath):
                shutil.copy(full_filepath, voice_data_dir)


        # generate
        logger.info("Copying completed. Starting building voice in %s" % (voice_dir))
        success = voice_build.generate_voice(voice_data_dir, voice_name, "cy") 


        #
        if not success:
            logger.info('Generate voice not successful') 
        else:
            logger.info('Generating voice completed and successful')
            voice_install(voice_name)
    else:
        logger.info("%s doesn't exist" % source_audio_dir)

    return success



def voice_install(voice_name):
    logger.info("Initiating installing voice in MaryTTS runtime API")    
    contents = urlopen("http://marytts-server-%s:8008/install?voice=%s" % (os.environ['MARYTTS_CY_VERSION'], voice_name)) 
    logger.info("Voice installed")

