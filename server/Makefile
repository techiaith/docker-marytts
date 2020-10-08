default: build

MARYTTS_CY_VERSION := 20.10
VOICES_DIR := ${PWD}/../voices

build:
	if [ ! -f "${VOICES_DIR}/installed-voices.txt" ]; then \
		echo "Copying default installed-voices.txt"; \
		cp installed-voices.txt ${VOICES_DIR}/; \
	fi
	docker build --rm -t techiaith/marytts-server:${MARYTTS_CY_VERSION} \
	--build-arg MARYTTS_CY_VERSION=${MARYTTS_CY_VERSION} \
	.


run:
	docker run --name marytts-server-${MARYTTS_CY_VERSION} --restart=always \
    	-d -p 52010:59125 \
		-v ${PWD}/../voices/:/voices \
	techiaith/marytts-server:${MARYTTS_CY_VERSION}


stop:
	docker stop marytts-server-${MARYTTS_CY_VERSION}
	docker rm marytts-server-${MARYTTS_CY_VERSION}


clean:
	docker rmi techiaith/marytts-server:${MARYTTS_CY_VERSION}




