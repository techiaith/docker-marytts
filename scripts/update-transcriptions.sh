#!/bin/bash

LIB_SRC="lib/modules/cy/lexicon"
MARYTTS_CY_SRC="src/main/resources/marytts/language/cy/lexicon"

lexicon_lts_pos_builder.sh ${LIB_SRC}/allophones.cy.xml ${LIB_SRC}/cy.txt

cp ${LIB_SRC}/allophones.cy.xml ${MARYTTS_CY_SRC}/
cp ${LIB_SRC}/cy.lts ${MARYTTS_CY_SRC}/
cp ${LIB_SRC}/cy_lexicon.fst ${MARYTTS_CY_SRC}/

find ${LIB_SRC} -type f -not -name '*.xml' -not -name '*.txt' -print0 | xargs -0 rm --
