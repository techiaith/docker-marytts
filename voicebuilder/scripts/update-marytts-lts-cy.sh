#!/bin/bash

LEXICON_GIT_URL="https://git.techiaith.bangor.ac.uk/lleferydd/ffoneteg/geiriadur-ynganu-bangor.git"
LEXICON_SRC="${MARYTTS_CY_HOME}/lib/modules/cy/lexicon"

MARYTTS_CY_SRC="${MARYTTS_CY_HOME}/src/main/resources/marytts/language/cy/lexicon"
MYDIR="$(dirname "${BASH_SOURCE[0]}")"

#
echo "--- Adapting lexicons for MaryTTS ... "
PYTHON_ADAPT_SCRIPT=${MYDIR}/python/adapt_lexicon.py
cat ${LEXICON_SRC}/geiriadur-ynganu-bangor/bangordict.dict ${LEXICON_SRC}/geiriadur-ynganu-bangor/bangordict.en.dict > ${LEXICON_SRC}/bangordict.cy_en.dict

cat ${LEXICON_SRC}/bangordict.cy_en.dict | python3 ${PYTHON_ADAPT_SCRIPT} ${LEXICON_SRC}/allophones.cy.xml > ${LEXICON_SRC}/bangor.g2p
cat ${LEXICON_SRC}/bangor.g2p | uniq > ${LEXICON_SRC}/cy.txt

#
echo "--- Training LTS models ---"
lexicon_lts_pos_builder.sh ${LEXICON_SRC}/allophones.cy.xml ${LEXICON_SRC}/cy.txt

cp ${LEXICON_SRC}/allophones.cy.xml ${MARYTTS_CY_SRC}/
cp ${LEXICON_SRC}/cy.lts ${MARYTTS_CY_SRC}/
cp ${LEXICON_SRC}/cy_lexicon.fst ${MARYTTS_CY_SRC}/

