#!/bin/sh

# EXIT ERROR settings 
set -o errexit

DESCRIPTION="Import an alternative clean text source into MySQL"

NUMARG=2
if [ $# -ne $NUMARG ]
then
  echo "NAME:
  	`basename $0`

DESCRIPTION:
    $DESCRIPTION

USAGE: 
	`basename $0` [config_file] [clean_text_to_import]
	
	config_file: wkdb config file  
	clean_text_to_import: a file containing clean text

EXAMPLE:
	`basename $0` /home/marytts/wikidump/wkdb.conf alt-cleantext/CofnodYCynulliad/CofnodYCynulliad.cy" 
  exit 1
fi  

# read variables from config file
CONFIG_FILE="`dirname "$1"`/`basename "$1"`"
. $CONFIG_FILE

BINDIR="`dirname "$0"`"
export MARY_BASE="`(cd "$BINDIR"/.. ; pwd)`"

CLEANTEXT_FILE=$2

python3 import-cleantext.py \
	$MYSQLHOST \
	$MYSQLUSER \
	$MYSQLPASSWD \
	$MYSQLDB \
	$LOCALE \
	$CLEANTEXT_FILE
	