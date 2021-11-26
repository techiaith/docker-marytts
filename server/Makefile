ls -default: build

MARYTTS_CY_VERSION := 21.03
VOICES_DIR := ${PWD}/../voices

build:
	if [ ! -f "${VOICES_DIR}/installed-voices.txt" ]; then \
		echo "Copying default installed-voices.txt"; \
		mkdir -p ${VOICES_DIR}/; \
		cp installed-voices.txt ${VOICES_DIR}/; \
	fi
	docker build --rm -t techiaith/marytts-server:${MARYTTS_CY_VERSION} \
		--build-arg MARYTTS_CY_VERSION=${MARYTTS_CY_VERSION} .


run:
	docker run --name marytts-server-${MARYTTS_CY_VERSION} --restart=always \
		-d -p 52010:59125 \
		-p 5301:8008 \
		-v ${PWD}/log:/var/log/marytts-server \
		-v ${VOICES_DIR}/:/voices \
		techiaith/marytts-server:${MARYTTS_CY_VERSION}


stop:
	-docker stop marytts-server-${MARYTTS_CY_VERSION}
	-docker rm marytts-server-${MARYTTS_CY_VERSION}
	sudo rm ${PWD}/log/*


clean:
	docker rmi techiaith/marytts-server:${MARYTTS_CY_VERSION}

