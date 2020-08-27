default: build


# --- MaryTTS voice building environment ------------------------------------------------------
build: inject_dockerfile_with_uid_gid 
	docker build --rm -t techiaith/marytts-voicebuild-gui .

inject_dockerfile_with_uid_gid: 
	./scripts/inject_uid_gid_into_dockerfile.sh

# add `--user marytts` if wanting to use GUI based voice import
run: mysql
	docker run --name marytts-voicebuild-gui -it \
 		-p 59126:59125 \
		--link marytts-mysql:mysql \
		-e DISPLAY=${DISPLAY} \
		--device /dev/snd \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v ${PWD}/recordings:/recordings \
		-v ${PWD}/../voices:/voices \
		-v ${PWD}/texts:/texts \
		-v ${PWD}/scripts:/opt/marytts/voicebuilder/scripts \
		-v ${PWD}/../marytts/marytts-languages/marytts-lang-cy:/opt/marytts/marytts-languages/marytts-lang-cy \
		techiaith/marytts-voicebuild-gui bash

stop:
	docker stop marytts-voicebuild-gui
	docker rm marytts-voicebuild-gui

clean:	
	docker rmi techiaith/marytts-voicebuild-gui




# --- MySQL -----------------------------------------------------------------------------------
mysql:
	docker run --name marytts-mysql --restart=always \
		-d -v ${PWD}/mysql:/var/lib/mysql \
		-e MYSQL_ROOT_PASSWORD=wiki123 \
		mysql:5.7

mysql-clean:
	-docker stop marytts-mysql
	-docker rm -v marytts-mysql
	sudo rm -rf mysql


