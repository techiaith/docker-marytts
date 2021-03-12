default: build

MARYTTS_CY_VERSION := 21.03

build:
	if [ ! -d "marytts" ]; then \
        	git clone https://github.com/techiaith/marytts.git; \
    	fi 	
	docker build --rm --build-arg BUILDARG_MARYTTS_CY_VERSION=${MARYTTS_CY_VERSION} -t techiaith/marytts:${MARYTTS_CY_VERSION} .


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

