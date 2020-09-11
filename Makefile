default: build

build: 
	if [ ! -d "marytts" ]; then \
            git clone https://github.com/techiaith/marytts.git; \
        fi 
	if [ ! -d "marytts/marytts-languages/marytts-lang-cy/lib/modules/cy/lexicon/geiriadur-ynganu-bangor" ]; then \
	    cd marytts/marytts-languages/marytts-lang-cy/lib/modules/cy/lexicon && git clone https://git.techiaith.bangor.ac.uk/lleferydd/ffoneteg/geiriadur-ynganu-bangor.git && git checkout v20.09; \
	else \
	    cd marytts/marytts-languages/marytts-lang-cy/lib/modules/cy/lexicon/geiriadur-ynganu-bangor && git pull; \
	fi 
	docker build --rm -t techiaith/marytts .

run:
	docker run --name marytts --restart=always \
    	-it  \
	-p 59125:59125 \
        -v ${PWD}/marytts/marytts-languages/marytts-lang-cy:/opt/marytts/marytts-languages/marytts-lang-cy \
	-v ${PWD}/voices/:/voices \
	techiaith/marytts bash

stop:
	docker stop marytts
	docker rm marytts

clean:
	docker rmi techiaith/marytts

