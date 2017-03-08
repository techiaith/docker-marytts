##!/bin/sh

# EXIT ERROR settings 
set -o errexit

DESCRIPTION="Export an clean text from MySQL to various formatted files"

NUMARG=2
if [ $# -ne $NUMARG ]
then
  echo "NAME:
        `basename $0`

DESCRIPTION:
    $DESCRIPTION

USAGE: 
        `basename $0` [config_file] [exported_clean_text_file]
        
        config_file: wkdb config file  
        exported_clean_text_file: the file containing exported text. *.csv or *.py recognised.

EXAMPLE:
        `basename $0` /home/marytts/wikidump/wkdb.conf selection.csv" 
  exit 1
fi

# read variables from config file
CONFIG_FILE="`dirname "$1"`/`basename "$1"`"
. $CONFIG_FILE

BINDIR="`dirname "$0"`"
export MARY_BASE="`(cd "$BINDIR"/.. ; pwd)`"

OUT_FILE=$2

python3 export-cleantext.py \
	$MYSQLHOST \
	$MYSQLUSER \
	$MYSQLPASSWD \
	$MYSQLDB \
	$LOCALE \
	$SELECTEDSENTENCESTABLENAME \
	$OUT_FILE
	