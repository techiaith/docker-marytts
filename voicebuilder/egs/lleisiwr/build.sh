#!/bin/bash

CWD_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

while getopts u: flag
do
    case "${flag}" in
        u) userid=${OPTARG};;
    esac
done

${MARYTTS_HOME}/target/marytts-${MARYTTS_VERSION}/bin/marytts-server &

rm -rf /voices/${userid}_cy
mkdir -p /voices/${userid}_cy/data
cp -v /data/lleisiwr/${userid}/* /voices/${userid}_cy/data/

python3 ${CWD_DIR}/../../scripts/python/voice_build.py -s /voices/${userid}_cy/data -v ${userid}_cy -l cy

