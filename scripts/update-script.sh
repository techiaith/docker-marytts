#!/bin/bash

SOURCE_DIR="/home/marytts/wikidump"
TARGET_DIR="/home/marytts/marytts-languages/marytts-lang-cy/script"

mkdir -p ${TARGET_DIR}

cp -rv ${SOURCE_DIR}/selection ${TARGET_DIR}/selection

cp ${SOURCE_DIR}/wkdb.conf ${TARGET_DIR}
cp ${SOURCE_DIR}/covDef.config ${TARGET_DIR}
cp ${SOURCE_DIR}/init.bin ${TARGET_DIR}
cp ${SOURCE_DIR}/selected.log ${TARGET_DIR}
cp ${SOURCE_DIR}/selected_text_transcription.log ${TARGET_DIR}
cp ${SOURCE_DIR}/overallLog.txt ${TARGET_DIR}

