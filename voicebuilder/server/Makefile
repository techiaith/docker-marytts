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
		-v ${PWD}/../../recordings/:/recordings \
		-v ${PWD}/../../voices:/opt/marytts/voices \
		techiaith/marytts-voicebuild-api:${MARYTTS_CY_VERSION}


stop:
	docker stop marytts-voicebuild-api-${MARYTTS_CY_VERSION}
	docker rm marytts-voicebuild-api-${MARYTTS_CY_VERSION}


clean:
	docker rmi techiaith/marytts-voicebuild-api:${MARYTTS_CY_VERSION}