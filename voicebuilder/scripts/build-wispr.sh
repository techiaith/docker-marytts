#!/bin/bash

CWD_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

${MARYTTS_HOME}/target/marytts-${MARYTTS_VERSION}/bin/marytts-server &

python3 ${CWD_DIR}/python/voice_build.py -v wispr -s /voices/wispr -l cy

