default: build-runtime

build-runtime: 
	docker build -t techiaith/marytts -f Dockerfile.runtime .

build-voicebuild: inject_dockerfile_with_uid_gid
	docker build -t techiaith/marytts -f Dockerfile.voicebuild .

build-voicebuild-api:
	docker build -t techiaith/marytts -f Dockerfile.voicebuildapi .


inject_dockerfile_with_uid_gid:
	./scripts/inject_uid_gid_into_dockerfile.sh

runtime:
	docker run --name marytts -p 59125:59125 -it \
		-v ${PWD}/voice-builder:/home/marytts/voice-builder \
		-v ${PWD}/texts:/home/marytts/texts \
		techiaith/marytts bash

voicebuild:
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

voicebuild-api:
	docker run --name marytts -it \
 		-p 8008:8008 \
		--link marytts-mysql:mysql \
		--link lleisiwr-mysql:lleisiwr_mysql \
		-v ${PWD}/voice-builder:/opt/marytts/voice-builder \
		-v ${PWD}/commonvoice-recordings:/commonvoice-recordings \
		-v ${PWD}/texts:/opt/marytts/texts \
		-v ${PWD}/marytts/marytts-languages/marytts-lang-cy:/opt/marytts/marytts-languages/marytts-lang-cy \
		techiaith/marytts bash

stop:
	docker stop marytts
	docker rm marytts

clean:
	docker rmi techiaith/marytts

mysql:
	docker run --name marytts-mysql -v ${PWD}/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=wiki123 -d mysql

mysql-clean:
	docker stop marytts-mysql
	docker rm -v marytts-mysql

github:
	git clone https://github.com/techiaith/marytts.git
	cd marytts && git checkout branch marytts-lang-cy
	 