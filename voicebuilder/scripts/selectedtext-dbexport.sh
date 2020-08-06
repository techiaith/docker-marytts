##!/bin/bash

# EXIT ERROR settings 
set -o errexit

DESCRIPTION="Export an clean text from MySQL to various formatted files"
MYDIR="$(dirname "${BASH_SOURCE[0]}")"

NUMARG=1
if [ $# -ne $NUMARG ]
then
  echo "NAME:
        `basename $0`

DESCRIPTION:
    $DESCRIPTION

USAGE: 
        `basename $0` [config_file] 
        
        config_file: wkdb config file  

EXAMPLE:
        `basename $0` /home/marytts/wikidump/wkdb.conf" 
  exit 1
fi

# read variables from config file
CONFIG_FILE="`dirname "$1"`/`basename "$1"`"
. $CONFIG_FILE

BINDIR="`dirname "$0"`"
export MARY_BASE="`(cd "$BINDIR"/.. ; pwd)`"

PYTHON_SCRIPT="${MYDIR}/python/export-cleantext.py"

OUT_FILE="/home/marytts/voice-builder/recorder/Prompts.py"
echo $OUT_FILE
python3 ${PYTHON_SCRIPT} \
	$MYSQLHOST \
	$MYSQLUSER \
	$MYSQLPASSWD \
	$MYSQLDB \
	$LOCALE \
	$SELECTEDSENTENCESTABLENAME \
	$OUT_FILE


OUT_FILE="/home/marytts/voice-builder/recorder/Prompts.txt"
echo $OUT_FILE
python3 ${PYTHON_SCRIPT} \
        $MYSQLHOST \
        $MYSQLUSER \
        $MYSQLPASSWD \
        $MYSQLDB \
        $LOCALE \
        $SELECTEDSENTENCESTABLENAME \
        $OUT_FILE

