import time
from celery import Celery

app = Celery('marytts_api_tasks', broker='pyamqp://guest@localhost//')

@app.task
def generate_voice(uid):
    time.sleep(60)
    
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

