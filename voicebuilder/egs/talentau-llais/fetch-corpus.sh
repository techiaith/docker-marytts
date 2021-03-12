#!/bin/bash
CWD_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DATA_SRC="https://git.techiaith.bangor.ac.uk/Data-Porth-Technolegau-Iaith/corpws-talentau-llais.git"

if [ ! -d "/data/corpws-talentau-llais" ]; then
	git clone ${DATA_SRC} /data/corpws-talentau-llais
fi
cd /data/corpws-talentau-llais && git pull
exit 0
