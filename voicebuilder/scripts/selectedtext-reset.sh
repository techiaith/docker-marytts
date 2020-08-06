##!/bin/bash

# EXIT ERROR settings 
set -o errexit

DESCRIPTION="Reset the database and associated files for repeated selections"
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

rm -rf init.bin covDef.config select* overallLog.txt || exit 1;

PYTHON_SCRIPT="${MYDIR}/reset-dbselectedtext.py"

python3 ${PYTHON_SCRIPT} \
	$MYSQLHOST \
	$MYSQLUSER \
	$MYSQLPASSWD \
	$MYSQLDB \
	$LOCALE \
	$SELECTEDSENTENCESTABLENAME 
	
