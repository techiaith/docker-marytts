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

#
. db_cy_3.conf
mkdir -p ${WIKIDATAPATH}
wkdb_featuremaker.sh db_cy_3.conf
wkdb_database_selector.sh db_cy_3.conf
selectedtext-dbexport.sh db_cy_3.conf

#
. db_cy_4.conf
mkdir -p ${WIKIDATAPATH}
wkdb_featuremaker.sh db_cy_4.conf
wkdb_database_selector.sh db_cy_4.conf
selectedtext-dbexport.sh db_cy_4.conf

#
. db_cy_5.conf
mkdir -p ${WIKIDATAPATH}
wkdb_featuremaker.sh db_cy_5.conf
wkdb_database_selector.sh db_cy_5.conf
selectedtext-dbexport.sh db_cy_5.conf

find /texts/commonvoice/cy -name marytts*.txt | xargs cp -vt /texts/commonvoice/cy