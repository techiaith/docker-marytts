default: build

MARYTTS_CY_VERSION := 20.10


build:
	docker build --rm -t techiaith/marytts-voicebuild-api:${MARYTTS_CY_VERSION} \
	--build-arg MARYTTS_CY_VERSION=${MARYTTS_CY_VERSION} \
	.


run:
	docker run --name marytts-voicebuild-api-${MARYTTS_CY_VERSION} --restart=always \
 		-d -p 32010:8008 \
		--link marytts-server-${MARYTTS_CY_VERSION}:marytts-server \
		-v ${PWD}/../../../docker-common-voice-lleisiwr/recordings/:/recordings/lleisiwr \
		-v ${PWD}/../../voices:/voices \
		-v ${PWD}/log:/var/log/voice-builder-api \
		techiaith/marytts-voicebuild-api:${MARYTTS_CY_VERSION}


stop:
	-docker stop marytts-voicebuild-api-${MARYTTS_CY_VERSION}
	-docker rm marytts-voicebuild-api-${MARYTTS_CY_VERSION}
	-sudo rm ${PWD}/log/*


clean:
	-docker rmi techiaith/marytts-voicebuild-api:${MARYTTS_CY_VERSION}
