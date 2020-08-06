#!/bin/bash
DATA_SRC="http://techiaith.cymru/lts/"
LEXICON_ROOT="${MARYTTS_CY_HOME}/lib/modules/cy/lexicon"
MYDIR="$(dirname "${BASH_SOURCE[0]}")"

# Check if the executables needed for this script are present in the system
command -v wget >/dev/null 2>&1 ||\
 { echo "\"wget\" is needed but not found"'!'; exit 1; }

echo "--- Starting data download ..."
wget -P ${LEXICON_ROOT} -N -nd -c -e robots=off -A txt,lexicon -r -np ${DATA_SRC} || \
 { echo "WGET error"'!' ; exit 1 ; }

PYTHON_SCRIPT=${MYDIR}/adapt-lexicon.py

cat ${LEXICON_ROOT}/cym.lexicon | uniq | python ${PYTHON_SCRIPT} > ${LEXICON_ROOT}/cy.txt

rm ${LEXICON_ROOT}/cym.lexicon
mv ${LEXICON_ROOT}/LICENSE.txt ${LEXICON_ROOT}/LEXICON_LICENSE.txt
