#!/bin/bash

DATA_SRC="https://raw.githubusercontent.com/mozilla/common-voice/main/server/data"
FILE_NAME="sentence-collector.txt"

VOICEBUILDER_SCRIPTS="/opt/marytts/voicebuilder/scripts"
COMMONVOICE_TEXTS="/texts/commonvoice"

rm -rf ${COMMONVOICE_TEXTS}

mkdir -p ${COMMONVOICE_TEXTS}/cy
mkdir -p ${COMMONVOICE_TEXTS}/en


echo "--- Starting data download ---"
wget -O ${COMMONVOICE_TEXTS}/cy/cy.txt ${DATA_SRC}/cy/${FILE_NAME} || { echo "WGET error"'!' ; exit 1 ; }
wget -O ${COMMONVOICE_TEXTS}/en/en.txt ${DATA_SRC}/en/${FILE_NAME} || { echo "WGET error"'!' ; exit 1 ; }

