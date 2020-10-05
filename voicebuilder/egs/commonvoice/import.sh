#!/bin/bash

DATA_SRC="https://raw.githubusercontent.com/mozilla/common-voice/main/server/data"
FILE_NAME="sentence-collector.txt"

VOICEBUILDER_SCRIPTS="/opt/marytts/voicebuilder/scripts"
COMMONVOICE_TEXTS="/texts/commonvoice"

mkdir -p ${COMMONVOICE_TEXTS}

# Check if the executables needed for this script are present in the system
command -v wget >/dev/null 2>&1 ||\
 { echo "\"wget\" is needed but not found"'!'; exit 1; }


echo "--- Starting data download ---"
wget -O ${COMMONVOICE_TEXTS}/cy.txt ${DATA_SRC}/cy/${FILE_NAME} || { echo "WGET error"'!' ; exit 1 ; }
wget -O ${COMMONVOICE_TEXTS}/en.txt ${DATA_SRC}/en/${FILE_NAME} || { echo "WGET error"'!' ; exit 1 ; }

echo "--- Creating MySQL database for texts --"
source ${VOICEBUILDER_SCRIPTS}/create-database-docker.sh db.conf

echo "--- Importing texts into MySQL ---"
cat ${COMMONVOICE_TEXTS}/cy.txt ${COMMONVOICE_TEXTS}/en.txt > ${COMMONVOICE_TEXTS}/cv.txt
source ${VOICEBUILDER_SCRIPTS}/alt-cleantext-import.sh db.conf ${COMMONVOICE_TEXTS}/cv.txt
