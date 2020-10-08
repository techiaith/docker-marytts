default: build

MARYTTS_CY_VERSION := 20.10


# --- MaryTTS headless/non-gui voice building api -------------------------------------
build-voicebuild-api: mysql
	docker build --rm -t techiaith/marytts-voicebuild-api:${MARYTTS_CY_VERSION} .

voicebuild-api:
	docker run --name marytts-voicebuild-api-${MARYTTS_CY_VERSION} --restart=always \
 		-d -p 8010:8008 \
		--link marytts-api:marytts-api \
		-v ${PWD}/../../recordings/:/recordings \	
		-v ${PWD}/../../voices:/opt/marytts/voices \
		techiaith/marytts-voicebuild-api:${MARYTTS_CY_VERSION}

stop-voicebuild-api:
	docker stop marytts-voicebuild-api-${MARYTTS_CY_VERSION}
	docker rm marytts-voicebuild-api-${MARYTTS_CY_VERSION}

clean-voicebuild-api:
	docker rmi techiaith/marytts-voicebuild-api:${MARYTTS_CY_VERSION}
