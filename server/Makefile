default: build

MARYTTS_CY_VERSION := 20.10

build: 	
	docker build --rm -t techiaith/marytts-server:${MARYTTS_CY_VERSION} \
	--build-arg MARYTTS_CY_VERSION=${MARYTTS_CY_VERSION} \
	.


run:
	docker run --name marytts-server-${MARYTTS_CY_VERSION} --restart=always \
    	-d -p 59200:59125 \
		-v ${PWD}/../voices/:/opt/marytts/voices \	
	techiaith/marytts-server:${MARYTTS_CY_VERSION}


stop:
	docker stop marytts-server-${MARYTTS_CY_VERSION}
	docker rm marytts-server-${MARYTTS_CY_VERSION}


clean:
	docker rmi techiaith/marytts-server:${MARYTTS_CY_VERSION}





# --- MaryTTS server/runtime with Python REST API  ----------------------------------------------------
build-runtime-api: build
	docker build --rm -t techiaith/marytts-api -f Dockerfile.runtimeapi .

runtime-api: 
	docker run --name marytts-api --restart=always \
    	-d -p 5300:8008  \		
		-v ${PWD}/../voices/:/opt/marytts/voices \
	techiaith/marytts-api

stop-runtime-api:
	docker stop marytts-api
	docker rm marytts-api

clean-runtime-api:
	docker rmi techiaith/marytts-api




# --- MaryTTS voice building environment ------------------------------------------------------
build-voicebuild: inject_dockerfile_with_uid_gid 
	docker build --rm -t techiaith/marytts-voicebuild -f Dockerfile.voicebuild .

inject_dockerfile_with_uid_gid: build
	./voice-builder/scripts/inject_uid_gid_into_dockerfile.sh

# add `--user marytts` if wanting to use GUI based voice import
voicebuild: mysql
	docker run --name marytts-voicebuild -it \
 		-p 59125:59125 \
		--link marytts-mysql:mysql \
		-e DISPLAY=${DISPLAY} \
		--device /dev/snd \
		--user marytts \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v ${PWD}/recordings:/recordings \
		-v ${PWD}/voices:/opt/marytts/voices \
		-v ${PWD}/texts:/opt/marytts/texts \
		-v ${PWD}/marytts/marytts-languages/marytts-lang-cy:/opt/marytts/marytts-languages/marytts-lang-cy \
		techiaith/marytts-voicebuild bash

stop-voicebuild:
	docker stop marytts-voicebuild
	docker rm marytts-voicebuild

clean-voicebuild:	
	docker rmi techiaith/marytts-voicebuild




# --- MaryTTS headless/non-gui voice building api -------------------------------------
build-voicebuild-api: mysql
	docker build --rm -t techiaith/marytts-voicebuild-api -f Dockerfile.voicebuildapi .

voicebuild-api:
	docker run --name marytts-voicebuild-api --restart=always \
 		-d -p 8008:8008 \
		--link marytts-api:marytts-api \
		-v ${PWD}/../docker-common-voice-lleisiwr/recordings/:/recordings/cy \
		-v ${PWD}/../docker-common-voice-lleisiwr-en/recordings/:/recordings/en_US \
		-v ${PWD}/voices:/opt/marytts/voices \
		-v ${PWD}/marytts/marytts-languages/marytts-lang-cy:/opt/marytts/marytts-languages/marytts-lang-cy \
		techiaith/marytts-voicebuild-api

stop-voicebuild-api:
	docker stop marytts-voicebuild-api
	docker rm marytts-voicebuild-api

clean-voicebuild-api:
	docker rmi techiaith/marytts-voicebuild-api




# --- MySQL -----------------------------------------------------------------------------------
mysql-run:
	docker run --name marytts-mysql --restart=always \
		-d -v ${PWD}/mysql:/var/lib/mysql \
		-e MYSQL_ROOT_PASSWORD=wiki123 \
		mysql

mysql-clean:
	docker stop marytts-mysql
	docker rm -v marytts-mysql




# --- Fetch MaryTTS CY source code from github ------------------------------------------------
github:
	git clone https://github.com/techiaith/marytts.git
	cd marytts && git checkout branch marytts-lang-cy
	 
