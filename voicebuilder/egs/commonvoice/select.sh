#!/bin/bash

COMMONVOICE_TEXTS="/texts/commonvoice"
VOICEBUILDER_SCRIPTS="/opt/marytts/voicebuilder/scripts"
source ${VOICEBUILDER_SCRIPTS}/selectedtext-reset.sh db.conf

wkdb_featuremaker.sh db.conf

wkdb_database_selector.sh db.conf

selectedtext-dbexport.sh db.conf