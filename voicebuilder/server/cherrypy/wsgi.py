#!/usr/bin/env python
import os
import shlex

import subprocess
import tempfile

import cherrypy
import logging

from voice_builder_api_tasks import generate_voice

class GenerateVoice(object):

    def __init__(self):
        self.startMaryTTS()

    def startMaryTTS(self):

        marytts_home = os.environ['MARYTTS_HOME']
        marytts_version = os.environ['MARYTTS_VERSION']
        marytts_base = os.path.join(marytts_home, 'target', "marytts-" + marytts_version)        
        cmd = 'java -showversion -Xms40m -Xmx1g -cp "%s/lib/*" -Dmary.base="%s" marytts.server.Mary' % (marytts_base, marytts_base,)
        popen_cmd = shlex.split(cmd)
        self.marytts_pid = subprocess.Popen(popen_cmd).pid
        cherrypy.log("Started MaryTTS server successfully pid:%s" % (self.marytts_pid))


    @cherrypy.expose
    def generate_voice(self, uid, locale, **kwargs):

        cherrypy.log("generating %s voice for '%s'" % (locale, uid))
        generate_voice.delay(uid, locale)
        cherrypy.log("generating voice request sent")


cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    'response.stream': True,
    'log.access_file': '/var/log/voice-builder-api/voice-builder-api.access.log',
    'log.error_file': '/var/log/voice-builder-api/voice-builder-api.error.log',
})

# Tell CherryPy to call "connect" for each thread, when it starts up 
#
cherrypy.tree.mount(GenerateVoice(), '/')
application = cherrypy.tree
