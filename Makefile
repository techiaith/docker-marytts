default: build-runtime


# --- Vanilla MaryTTS server/runtime ----------------------------------------------------------

build-runtime: 
	docker build --rm -t techiaith/marytts -f Dockerfile.runtime .

runtime:
	docker run --name marytts --restart=always \
    -d -p 59125:59125 \
		-v ${PWD}/voice-builder:/home/marytts/voice-builder \
		techiaith/marytts 

stop:
	docker stop marytts
	docker rm marytts

clean:
	docker rmi techiaith/marytts


# --- MaryTTS voice building environment ------------------------------------------------------

build-voicebuild: inject_dockerfile_with_uid_gid
	docker build --rm -t techiaith/marytts-voicebuild -f Dockerfile.voicebuild .

inject_dockerfile_with_uid_gid:
	./scripts/inject_uid_gid_into_dockerfile.sh

voicebuild: mysql
	docker run --name marytts -it \
 		-p 59125:59125 \
		--link marytts-mysql:mysql \
		-e DISPLAY=${DISPLAY} \
		--device /dev/snd \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v ${PWD}/voice-builder:/home/marytts/voice-builder \
		-v ${PWD}/texts:/home/marytts/texts \
		-v ${PWD}/marytts/marytts-languages/marytts-lang-cy:/home/marytts/marytts-languages/marytts-lang-cy \
		techiaith/marytts bash



# --- MaryTTS headless/non-gui voice building environment -------------------------------------

build-voicebuild-api: mysql
	docker build --rm -t techiaith/marytts-voicebuild-api -f Dockerfile.voicebuildapi .

voicebuild-api:
	docker run --name marytts-voicebuild-api --restart=always \
 		-d -p 8008:8008 \
		--link marytts-mysql:mysql \
		--link lleisiwr-mysql:lleisiwr_mysql \
		-v ${PWD}/voice-builder/:/opt/marytts/voice-builder \
		-v ${PWD}/../docker-common-voice-lleisiwr/recordings/:/commonvoice-recordings \
		-v ${PWD}/../docker-common-voice-lleisiwr-en/recordings/:/commonvoice-recordings-en \
		-v ${PWD}/texts/:/opt/marytts/texts \
		-v ${PWD}/marytts/marytts-languages/marytts-lang-cy:/opt/marytts/marytts-languages/marytts-lang-cy \
		techiaith/marytts

stop-voicebuild-api:
	docker stop marytts-voicebuild-api
	docker rm marytts-voicebuild-api

clean-voicebuild-api:
	docker stop marytts-voicebuild-api
	docker rm marytts-voicebuild-api


# --- MaryTTS Server with Python REST API  ----------------------------------------------------

build-runtime-api: build-runtime
	docker build --rm -t techiaith/marytts-api -f Dockerfile.runtimeapi .

runtime-api:
	docker run --name marytts-api --restart=always \
    -d -p 5300:8008 -p 59125:59125 \
		-v ${PWD}/voice-builder/:/opt/marytts/voice-builder \
		techiaith/marytts-api

stop-runtime-api:
	docker stop marytts-api
	docker rm marytts-api

clean-runtime-api:
	docker rmi techiaith/marytts-api




# --- MySQL -----------------------------------------------------------------------------------

mysql:
	docker run --name marytts-mysql -v ${PWD}/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=wiki123 -d mysql


mysql-clean:
	docker stop marytts-mysql
	docker rm -v marytts-mysql


# --- Fetch MaryTTS CY source code from github ------------------------------------------------
github:
	git clone https://github.com/techiaith/marytts.git
	cd marytts && git checkout branch marytts-lang-cy
	 
