##!/bin/sh

# EXIT ERROR settings 
set -o errexit

DESCRIPTION="Initialise voice building environment with recordings"
MYDIR="$(dirname "${BASH_SOURCE[0]}")"

NUMARG=1
if [ $# -ne $NUMARG ]
then
  echo "NAME:
        `basename $0`

DESCRIPTION:
    $DESCRIPTION

USAGE: 
        `basename $0` [voice_name] 
        
        voice_name: name of the new voice

EXAMPLE:
        `basename $0` macsen" 
  exit 1
fi

# read variables from config file
VOICE_NAME=$1

mkdir -p ../${VOICE_NAME}/recordings
python3 Common-Voice-Import.py audio
cp txt.done.data ../${VOICE_NAME}
cp audio/* ../${VOICE_NAME}/recordings

echo "Creating config files for voice-import...."
cp importMain.config.template ../${VOICE_NAME}/importMain.config
sed s/VOICENAME/${VOICE_NAME}/g database.config.template > ../${VOICE_NAME}/database.config
