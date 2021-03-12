#!/bin/bash

CWD_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

while getopts u: flag
do
    case "$flag" in
        u) userid=${OPTARG};;
    esac
done

nohup ${MARYTTS_HOME}/target/marytts-${MARYTTS_VERSION}/bin/marytts-server >> ${MARYTTS_HOME}/err.log 2>&1 &

echo "clean voice dir /voices/${userid}"
rm -rf /voices/${userid}
mkdir -p /voices/${userid}/data
mkdir -p /voices/${userid}/data/normalized

echo "copying "`ls /data/corpws-talentau-llais/${userid}/*.wav | wc -l` " files from /data/corpws-talentau-llais/${userid}"
for f in /data/corpws-talentau-llais/${userid}/*;do cp "$f" /voices/${userid}/data/;done
cp importMain.config /voices/${userid}/

python3 ${CWD_DIR}/../../scripts/python/voice_build.py -s /voices/${userid}/data -v ${userid} -l cy
exit 0
