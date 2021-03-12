default: build

MARYTTS_CY_VERSION := 21.03
BANGORDICT_BRANCH := master

# --- MaryTTS voice building environment ------------------------------------------------------
build: inject_dockerfile_with_uid_gid
	if [ ! -d "../marytts/marytts-languages/marytts-lang-cy/lib/modules/cy/lexicon/geiriadur-ynganu-bangor" ]; then \
	    cd ../marytts/marytts-languages/marytts-lang-cy/lib/modules/cy/lexicon && git clone https://github.com/techiaith/geiriadur-ynganu-bangor.git && cd geiriadur-ynganu-bangor && git checkout ${BANGORDICT_BRANCH}; \
	else \
	    cd ../marytts/marytts-languages/marytts-lang-cy/lib/modules/cy/lexicon/geiriadur-ynganu-bangor && git pull && git checkout ${BANGORDICT_BRANCH}; \
	fi 
	docker build --rm --build-arg BUILDARG_MARYTTS_CY_VERSION=${MARYTTS_CY_VERSION} -t techiaith/marytts-voicebuild:${MARYTTS_CY_VERSION} .


inject_dockerfile_with_uid_gid: 
	./scripts/inject_uid_gid_into_dockerfile.sh

# add `--user marytts` if wanting to use GUI based voice import
run: mysql
	docker run --name marytts-voicebuild-${MARYTTS_CY_VERSION} -it \
 		-p 59136:59125 \
		--link marytts-mysql-${MARYTTS_CY_VERSION}:mysql \
		-e DISPLAY=${IP}:0 \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v ${PWD}/data:/data \
		-v ${PWD}/../voices:/voices \
		-v ${PWD}/texts:/texts \
		-v ${PWD}/scripts:/opt/marytts/voicebuilder/scripts \
		-v ${PWD}/egs:/opt/marytts/voicebuilder/egs \
		-v ${PWD}/../marytts/marytts-languages/marytts-lang-cy:/opt/marytts/marytts-languages/marytts-lang-cy \
		techiaith/marytts-voicebuild:${MARYTTS_CY_VERSION} bash

stop:
	-docker stop marytts-voicebuild-${MARYTTS_CY_VERSION}
	-docker rm marytts-voicebuild-${MARYTTS_CY_VERSION}

clean:	
	-docker rmi techiaith/marytts-voicebuild:${MARYTTS_CY_VERSION}




# --- MySQL -----------------------------------------------------------------------------------
mysql:
	docker run --name marytts-mysql-${MARYTTS_CY_VERSION} --restart=always \
		-d -v ${PWD}/mysql/${MARYTTS_CY_VERSION}:/var/lib/mysql \
		-e MYSQL_ROOT_PASSWORD=wiki123 \
		mysql:5.7

mysql-clean:
	-docker stop marytts-mysql-${MARYTTS_CY_VERSION}
	-docker rm -v marytts-mysql-${MARYTTS_CY_VERSION}
	sudo rm -rf mysql/${MARYTTS_CY_VERSION}
