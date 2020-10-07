#!/bin/bash
set -e

COMMONVOICE_TEXTS="/texts/commonvoice/en"
VOICEBUILDER_SCRIPTS="/opt/marytts/voicebuilder/scripts"

LEXICON_SRC="${MARYTTS_CY_HOME}/lib/modules/cy/lexicon"

MARYTTS_CY_SRC="${MARYTTS_CY_HOME}/src/main/resources/marytts/language/cy/lexicon"
MYDIR="$(dirname "${BASH_SOURCE[0]}")"

PYTHON_LEXICON_ADAPT_SCRIPT=${MARYTTS_CY_HOME}/bin/python/adapt_lexicon.py


# Creating/Reset MySQL database for texts
source ${VOICEBUILDER_SCRIPTS}/create-database-docker.sh db_en.conf


#  Importing texts into MySQL
source ${VOICEBUILDER_SCRIPTS}/alt-cleantext-import.sh db_en.conf ${COMMONVOICE_TEXTS}/en.txt


# create a new LTS lexicon and model based on CMUDict with Welsh phonemes
cat ${LEXICON_SRC}/geiriadur-ynganu-bangor/cmudict.dict | python3 ${PYTHON_LEXICON_ADAPT_SCRIPT} ${LEXICON_SRC}/allophones.cy.xml > ${LEXICON_SRC}/bangor.g2p
cat ${LEXICON_SRC}/bangor.g2p | uniq > ${LEXICON_SRC}/cy.txt


# Training new LTS models
lexicon_lts_pos_builder.sh ${LEXICON_SRC}/allophones.cy.xml ${LEXICON_SRC}/cy.txt

cp ${LEXICON_SRC}/allophones.cy.xml ${MARYTTS_CY_SRC}/
cp ${LEXICON_SRC}/cy.lts ${MARYTTS_CY_SRC}/
cp ${LEXICON_SRC}/cy_lexicon.fst ${MARYTTS_CY_SRC}/

ls -l ${MARYTTS_CY_SRC}

# Rebuild MaryTTS with the new LTS lexicon
cd ${MARYTTS_CY_HOME}/../..

mvn install

cp -v ${MARYTTS_CY_HOME}/target/marytts-lang-cy-${MARYTTS_VERSION}.jar ${MARYTTS_HOME}/target/marytts-${MARYTTS_VERSION}/lib
cp -v ${MARYTTS_CY_HOME}/target/marytts-lang-cy-${MARYTTS_VERSION}.jar ${MARYTTS_HOME}/target/marytts-builder-${MARYTTS_VERSION}/lib
cp -v ${MARYTTS_CY_HOME}/marytts-lang-cy-${MARYTTS_VERSION}-component.xml ${MARYTTS_HOME}/target/marytts-${MARYTTS_VERSION}/installed

cd -

# Select sentences with new LTS lexicon and model from MySQL texts.
wkdb_featuremaker.sh db_en.conf

wkdb_database_selector.sh db_en.conf

selectedtext-dbexport.sh db_en.conf
