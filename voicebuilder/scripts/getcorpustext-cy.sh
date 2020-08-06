#!/bin/bash

usage() { echo "Usage: $0 -n <corpus name>" 1>&2; exit 1; }

DATA_SRC="http://techiaith.cymru/corpws/Testunau"
TEXT_LANG="cy"

while getopts "n:" o; do
	case "${o}" in
		n)
			NAME=${OPTARG}		
			echo "Name of model/engine/collection : ${NAME}" 
			;;
		*)
			usage	
			;;
	esac
done  
shift $((OPTIND-1))

if [ -z "${NAME}" ]; then
    usage
fi

mkdir -p alt-cleantext/${NAME}

# Check if the executables needed for this script are present in the system
command -v wget >/dev/null 2>&1 ||\
 { echo "\"wget\" is needed but not found"'!'; exit 1; }

echo "--- Starting data download ..."

cd alt-cleantext/${NAME}

wget -O - ${DATA_SRC}/${NAME}.tar.gz | tar -zxf - || \
 { echo "WGET error"'!' ; exit 1 ; }

find . -type f -not -name '*.'${TEXT_LANG} | xargs rm

cd -
