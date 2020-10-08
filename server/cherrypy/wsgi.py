#!/usr/bin/env python
import os
import sys
import signal
import shlex
import subprocess
import codecs

import cherrypy
import logging
import tempfile

import http.client
import urllib
 
class MaryTTSAPI(object):

    def __init__(self):
                
        self.marytts_host = "127.0.0.1"
        self.marytts_port = 59125

        self.marytts_pid = 0

        self.installed_voices = []
        self.reinstall_voices_from_manifest()

        self.startMaryTTS()


    def startMaryTTS(self):

        if self.marytts_pid == 0:
            marytts_home = os.environ['MARYTTS_HOME']
            marytts_version = os.environ['MARYTTS_VERSION']
            marytts_base = os.path.join(marytts_home, 'target', "marytts-" + marytts_version)

            cherrypy.log("Starting MaryTTS Server...")
            cmd = 'java -showversion -Xms40m -Xmx1g -cp "%s/lib/*" -Dmary.base="%s" marytts.server.Mary' % (marytts_base, marytts_base,)
            popen_cmd = shlex.split(cmd)
            self.marytts_pid = subprocess.Popen(popen_cmd).pid

            cherrypy.log("Started MaryTTS server successfully pid:%s" % (self.marytts_pid))
    

    def stopMaryTTS(self):
        if self.marytts_pid > 0:
            cherrypy.log("Stopping MaryTTS Server...")
            os.kill(self.marytts_pid, signal.SIGKILL)
            self.marytts_pid = 0
            cherrypy.log("Stopped MaryTTS Server successfully.")


    def ttsToMp3(self, voice, lang, text):
        with tempfile.NamedTemporaryFile() as wavfile:

            wavfile.write(self.exec_marytts_generate(voice, lang, text))
            wavfile.flush()

            cmd = "lame --quiet -V 9 %s -" % wavfile.name

            mp3_file = tempfile.SpooledTemporaryFile(max_size=4*1024*1024, mode='wb')
            mp3_file.write(subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read())
            mp3_file.seek(0)
                
            return mp3_file


    def ttsToWav(self, voice, lang, text):
        tmp_file = tempfile.SpooledTemporaryFile(max_size=4*1024*1024, mode='wb')
        tmp_file.write(self.exec_marytts_generate(voice, lang, text))
        tmp_file.seek(0)
        return tmp_file


    @cherrypy.expose
    def download(self, voice, **kwargs):
        self.stopMaryTTS()
        cmd = "voice-download.sh %s" % voice
        subprocess.Popen(cmd, shell=True).wait()
        self.startMaryTTS()


    @cherrypy.expose
    def install(self, voice, **kwargs):
        self.stopMaryTTS()

        self.add_voice_to_manifest(voice)
        self.exec_marytts_voice_install(voice)

        self.startMaryTTS()


    def add_voice_to_manifest(self, voice):
        marytts_voices_home = os.environ['MARYTTS_VOICES_HOME']
        with codecs.open(os.path.join(marytts_voices_home, 'installed-voices.txt'), 'a', encoding='utf-8') as voices_manifest:
            voices.manifest.write(voice + '\n')
            self.installed_voices.append(voice)
       
       
    def reinstall_voices_from_manifest(self):
        marytts_voices_home = os.environ['MARYTTS_VOICES_HOME']
        with codecs.open(os.path.join(marytts_voices_home, 'installed-voices.txt'), 'r', encoding='utf-8') as voices_manifest:
            for voice in voices_manifest:
                cherrypy.log("reinstalling voice : %s " % voice)
                self.installed_voices.append(voice.strip())
                self.exec_marytts_voice_install(voice)

 
    def exec_marytts_voice_install(self, voice):
        cmd = "voice-install-cy.sh %s" % voice
        subprocess.Popen(cmd, shell=True).wait()


    def exec_marytts_generate(self, voice, lang, text):
        """Given a message in message,
           return a response in the appropriate
           format."""

        raw_params = {"INPUT_TEXT": text,
                "INPUT_TYPE": "TEXT",
                "OUTPUT_TYPE": "AUDIO",
                "LOCALE": lang,
                "AUDIO": "WAVE_FILE",
                "VOICE": voice,
                }

        cherrypy.log("marytts request: %s " % raw_params)
        params = urllib.urlencode(raw_params)
        headers = {}

        # Open connection to self.host, self.port.
        conn = http.client.HTTPConnection(self.marytts_host, self.marytts_port)

        #conn.set_debuglevel(5)
        
        conn.request("POST", "/process", params, headers)
        response = conn.getresponse()
        if response.status != 200:
            #print response.getheaders()
            raise RuntimeError("{0}: {1}".format(response.status, response.reason))
        return response.read()


    @cherrypy.expose
    def speak(self, text, uid='wispr', lang='cy', format='mp3', **kwargs):
        
        cherrypy.log("%s speaking '%s'" % (uid, text))

        try:
            format = format.lower()
            if format not in ('mp3', 'wav'):
                raise ValueError("'format' must be either 'mp3' or 'wav")
            if lang not in ('cy', 'en_US'):
                raise ValueError("'lang' must be either 'cy' or 'en_US'")
        except ValueError as e:
            return "ERROR: %s" % str(e)
      
        is_wispr = (uid.lower() == 'wispr')
        if is_wispr:
            voice = uid
        else:
            voice = uid + "_" + lang 
            if voice in self.installed_voices:
                voice = uid + "_" + lang.lower()
            else:
                voice = 'wispr'
            
        is_mp3 = (format.lower() == 'mp3')
        if is_mp3:
            tmpfile = self.ttsToMp3(voice, lang, text.encode('utf-8'))
        else:
            tmpfile = self.ttsToWav(voice, lang, text.encode('utf-8'))

        cherrypy.response.headers["Content-Type"] = "audio/%s" % ('mpeg' if is_mp3 else 'wav')
        return tmpfile.read()


cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    'response.stream': True,
    'log.error_file': 'marytts-api.log',
})

cherrypy.tree.mount(MaryTTSAPI(), '/')
application = cherrypy.tree

