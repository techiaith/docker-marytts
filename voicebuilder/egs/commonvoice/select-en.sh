#!/bin/bash
set -e

# Select sentences with new LTS lexicon and model from MySQL texts.
. db_en_1.conf
mkdir -p ${WIKIDATAPATH}
wkdb_featuremaker.sh db_en_1.conf
wkdb_database_selector.sh db_en_1.conf
selectedtext-dbexport.sh db_en_1.conf

#   
. db_en_2.conf
mkdir -p ${WIKIDATAPATH}
wkdb_featuremaker.sh db_en_2.conf
wkdb_database_selector.sh db_en_2.conf
selectedtext-dbexport.sh db_en_2.conf
