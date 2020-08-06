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


    @cherrypy.expose
    def index(self):
        return """
<html>
<head>
<script type='text/javascript'>
function generate() {
    var uid = document.getElementById('uid').value.trim();
    var locale = document.getElementById('lang').value.trim();
    var audioElement = document.createElement('audio');
    var url = location.href + 'generate_voice?uid=' + encodeURI(uid) + '&locale=' + encodeURI(locale)
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

<h1>DEMO CREU LLAIS TESTUN-I-LEFERYDD MARYTTS ~ MARYTTS TEXT-TO-SPEECH GENERATE DEMO</h1>

<textarea id='uid' placeholder="Ysgrifennwch uid y llais"></textarea>
<textarea id='lang' placeholder="Ysgrifennwch iaith y llais ('cy' neu 'en_US')"></textarea>

<p>
<button onclick="generate()">Cynhyrchu / Generate</button>
</p>

"""

cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    'response.stream': True,
    'log.access_file': 'voice-builder-api.access.log',
    'log.error_file': 'voice-builder-api.error.log',
})

# Tell CherryPy to call "connect" for each thread, when it starts up 
#
cherrypy.tree.mount(GenerateVoice(), '/')
application = cherrypy.tree