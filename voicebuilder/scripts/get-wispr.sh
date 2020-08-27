#!/bin/bash
CWD_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DATA_SRC="https://git.techiaith.bangor.ac.uk/Data-Porth-Technolegau-Iaith/Corpws-WISPR.git"

git clone ${DATA_SRC} /recordings/Corpws-WISPR

python3 ${CWD_DIR}/python/convert_wispr_to_marytts.py

