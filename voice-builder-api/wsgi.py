#!/usr/bin/env python
import cherrypy
import logging

import subprocess
import tempfile
import os

from voice_builder_api_tasks import generate_voice

class GenerateVoice(object):

    def __init__(self):
        pass
 
    def error_page_default(status, message, traceback, version):
        """Handles any server errors, and returns a json response back to the user"""
        return u"ERROR %s: %s" % (status, message)

    @cherrypy.expose
    def generate_voice(self, uid, **kwargs):

        cherrypy.log("generating voice for '%s'" % uid)
        generate_voice.delay(uid)
        cherrypy.log("generating voice request sent")


    @cherrypy.expose
    def index(self):
        return """
<html>
<head>
<script type='text/javascript'>
function llefaru() {
    var testun = document.getElementById('llais').value.trim();
    var audioElement = document.createElement('audio');
    var url = location.href + 'generate_voice?uid=' + encodeURI(testun)
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

<textarea id='llais' placeholder="Ysgrifennwch uid y llais"></textarea>

<p>
<button onclick="llefaru()">Cynhyrchu / Generate</button>
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
