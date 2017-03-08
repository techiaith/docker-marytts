#!/bin/bash

DATA_SRC="http://techiaith.cymru/lts/"
LEXICON_ROOT="/home/marytts/marytts-languages/marytts-lang-cy/lib/modules/cy/lexicon"

# Check if the executables needed for this script are present in the system
command -v wget >/dev/null 2>&1 ||\
 { echo "\"wget\" is needed but not found"'!'; exit 1; }

echo "--- Starting data download ..."
wget -P ${LEXICON_ROOT} -N -nd -c -e robots=off -A txt,lexicon -r -np ${DATA_SRC} || \
 { echo "WGET error"'!' ; exit 1 ; }

cat ${LEXICON_ROOT}/cym.lexicon | uniq | python adapt-lexicon.py > ${LEXICON_ROOT}/cy.txt

rm ${LEXICON_ROOT}/cym.lexicon
mv ${LEXICON_ROOT}/LICENSE.txt ${LEXICON_ROOT}/LEXICON_LICENSE.txt
