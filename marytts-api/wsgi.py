#!/usr/bin/env python
import os
import signal
import shlex
import subprocess

import cherrypy
import logging
import tempfile
import maryclient

class MaryTTSAPI(object):

    def __init__(self):
                
        self.marytts_pid = 0
        self.maryttsclient = maryclient.maryclient()

        self.startMaryTTS()

        
    def startMaryTTS(self):
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


    def ttsToMp3(self, text):
        with tempfile.NamedTemporaryFile() as wavfile:
            wavfile.write(self.maryttsclient.generate(text))
            wavfile.flush()

            cmd = "lame --quiet -V 9 %s -" % wavfile.name

            mp3_file = tempfile.SpooledTemporaryFile(max_size=4*1024*1024, mode='wb')
            mp3_file.write(subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read())
            mp3_file.seek(0)
                
            return mp3_file


    def ttsToWav(self, text):
        tmp_file = tempfile.SpooledTemporaryFile(max_size=4*1024*1024, mode='wb')
        tmp_file.write(self.maryttsclient.generate(text))
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

        cmd = "voice-install-cy.sh %s" % voice
        subprocess.Popen(cmd, shell=True).wait()
        
        self.startMaryTTS()


    @cherrypy.expose
    def speak(self, text, format='mp3', **kwargs):
        
        cherrypy.log("speaking '%s'" % text)

        try:
            format = format.lower()
            if format not in ('mp3', 'wav'):
                raise ValueError("'format' must be either 'mp3' or 'wav")
        except ValueError as e:
            return "ERROR: %s" % str(e)

        is_mp3 = (format.lower() == 'mp3')
        tmpfile = self.ttsToMp3(text.encode('utf-8')) if is_mp3 else self.ttsToWav(text.encode('utf-8'))

        cherrypy.response.headers["Content-Type"] = "audio/%s" % ('mpeg' if is_mp3 else 'wav')
        return tmpfile.read()


    @cherrypy.expose
    def index(self):
	return """
<html>
<head>
<script type='text/javascript'>
function llefaru() {
    var testun = document.getElementById('llais').value.trim();
    var audioElement = document.createElement('audio');
    var url = location.href + 'speak?text=' + encodeURIComponent(testun)    
    audioElement.setAttribute('src', url);
    audioElement.play();
}
</script>
<style>
.logos {
 	background-color: #333333;
    	height: 90px;
}

.uti {
    float: left;
    padding-left: 32px;
    padding-top: 12px;
}

.pb {
    float: right;
    padding-right: 24px;
    padding-top: 12px;
}

h1, p, textarea {
 	font-family: "Vectora W02_55 Roman","Voces";
}

#llais {
        width:100%;
        display:block;
	padding:10px;
}

</style>
</head>
<body>
<div class="logos">
	<div class="uti"><a href="http://www.bangor.ac.uk"><img src="http://techiaith.cymru/wp-content/uploads/2017/10/pb.jpg"></a></div>
	<div class="pb"><a href="http://techiaith.bangor.ac.uk"><img src="http://techiaith.cymru/wp-content/uploads/2017/10/uti.jpg"></a></div>
</div>

<h1>DEMO TESTUN-I-LEFERYDD MARYTTS ~ MARYTTS TEXT-TO-SPEECH DEMO</h1>

<textarea id='llais' placeholder="Ysgrifennwch rhywbeth i'w llefaru"></textarea>

<p>
<button onclick="llefaru()">Chwarae / Play</button>
</p>

"""

cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    'response.stream': True,
    'log.error_file': 'marytts-api.log',
})

cherrypy.tree.mount(MaryTTSAPI(), '/')
application = cherrypy.tree
