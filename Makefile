default: build

MARYTTS_CY_VERSION := 20.10


build: 
	if [ ! -d "marytts" ]; then \
        git clone https://git.techiaith.bangor.ac.uk/lleferydd/marytts.git; \
    fi 
	if [ ! -d "marytts/marytts-languages/marytts-lang-cy/lib/modules/cy/lexicon/geiriadur-ynganu-bangor" ]; then \
	    cd marytts/marytts-languages/marytts-lang-cy/lib/modules/cy/lexicon && git clone https://git.techiaith.bangor.ac.uk/lleferydd/ffoneteg/geiriadur-ynganu-bangor.git && git checkout issue_5; \
	else \
	    cd marytts/marytts-languages/marytts-lang-cy/lib/modules/cy/lexicon/geiriadur-ynganu-bangor && git pull && git checkout issue_5; \
	fi 
	docker build --rm -t techiaith/marytts:${MARYTTS_CY_VERSION} .


run:
	docker run --name marytts-${MARYTTS_CY_VERSION} --restart=always \
    	-it  \
	-p 59135:59125 \
        -v ${PWD}/marytts/marytts-languages/marytts-lang-cy:/opt/marytts/marytts-languages/marytts-lang-cy \
	-v ${PWD}/voices/:/voices \
	techiaith/marytts:${MARYTTS_CY_VERSION} bash


stop:
	-docker stop marytts-${MARYTTS_CY_VERSION}
	-docker rm marytts-${MARYTTS_CY_VERSION}


clean:
	-docker rmi techiaith/marytts:${MARYTTS_CY_VERSION}

