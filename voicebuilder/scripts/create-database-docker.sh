#!/bin/bash

##################################
# create_database_docker.sh
##################################

# EXIT ERROR settings
set -xo errexit

DESCRIPTION="mysql database creation"

NUMARG=1
if [ $# -ne $NUMARG ]
then
  echo "NAME:
        `basename $0`

DESCRIPTION:
    $DESCRIPTION

USAGE:
        `basename $0` [config_file]
        config_file: wkdb config file

EXAMPLE:
        `basename $0` /home/mary/wikidb_data/wkdb.conf"
  exit 1
fi

# read variables from config file
CONFIG_FILE="`dirname "$1"`/`basename "$1"`"
. $CONFIG_FILE

echo $MYSQLHOST, $MYSQLUSER, $MYSQLPASSWD, $MYSQLDB

# DB CREATION
mysql --host=$MYSQLHOST --user="root" --password=$MYSQLPASSWD -e \
"create database if not exists $MYSQLDB;" 

mysql --host=$MYSQLHOST --user="root" --password=$MYSQLPASSWD -e \
"SET GLOBAL sql_mode='';select @@GLOBAL.sql_mode;"


mysql --host=$MYSQLHOST --user="root" --password=$MYSQLPASSWD -e \
"grant all privileges on $MYSQLDB.* to '$MYSQLUSER'@'%' with grant option; \
flush privileges;"

echo "$MYSQLDB database has been created at host $MYSQLHOST, all privileges are granted to user $MYSQLUSER in the $MYSQLHOST and the password $MYSQLPASSWD"

mysql --host=$MYSQLHOST --user="root" --password=$MYSQLPASSWD --database=$MYSQLDB -e \
"DROP TABLE IF EXISTS ${LOCALE}_cleanText;"

mysql --host=$MYSQLHOST --user="root" --password=$MYSQLPASSWD --database=$MYSQLDB -e \
"DROP TABLE IF EXISTS ${LOCALE}_dbselection;"

mysql --host=$MYSQLHOST --user="root" --password=$MYSQLPASSWD --database=$MYSQLDB -e \
"DROP TABLE IF EXISTS tablesDescription;"

mysql --host=$MYSQLHOST --user="root" --password=$MYSQLPASSWD --database=$MYSQLDB -e \
"DROP TABLE IF EXISTS ${LOCALE}_${SELECTEDSENTENCESTABLENAME}_selectedSentences;"

mysql --host=$MYSQLHOST --user="root" --password=$MYSQLPASSWD --database=$MYSQLDB -e \
"CREATE TABLE IF NOT EXISTS ${LOCALE}_cleanText (id int UNSIGNED NOT NULL AUTO_INCREMENT, \
                 cleanText MEDIUMBLOB NOT NULL, processed BOOLEAN, page_id int UNSIGNED NOT NULL, \
                 text_id int UNSIGNED NOT NULL, PRIMARY KEY id (id) \
                 ) MAX_ROWS=250000 AVG_ROW_LENGTH=10240 CHARACTER SET utf8;"

echo "$MYSQLDB::${LOCALE}_cleanText has been created"
