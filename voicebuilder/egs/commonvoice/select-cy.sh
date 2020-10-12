#!/bin/bash
set -e

# Select sentences with new LTS lexicon and model from MySQL texts.
. db_cy_1.conf
mkdir -p ${WIKIDATAPATH}
wkdb_featuremaker.sh db_cy_1.conf
wkdb_database_selector.sh db_cy_1.conf
selectedtext-dbexport.sh db_cy_1.conf

#   
. db_cy_2.conf
mkdir -p ${WIKIDATAPATH}
wkdb_featuremaker.sh db_cy_2.conf
wkdb_database_selector.sh db_cy_2.conf
selectedtext-dbexport.sh db_cy_2.conf
