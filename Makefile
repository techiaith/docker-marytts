default: build

build:
	docker build -t techiaith/marytts .

run:
	if [ ! -f text/wkdb.conf ] ; \
	then \
		cp wkdb.conf text/; \
	fi;
	docker run --name marytts -p 59125:59125 -it --link marytts-mysql:mysql -e DISPLAY=${DISPLAY} -v /tmp/.X11-unix:/tmp/.X11-unix -v ${PWD}/audio:/home/marytts/marytts-languages/marytts-lang-cy/scripts/audio -v ${PWD}/text:/home/marytts/text techiaith/marytts bash

stop:
	docker stop marytts
	docker rm marytts

clean:
	docker rmi techiaith/marytts

mysql:
	docker run --name marytts-mysql -e MYSQL_ROOT_PASSWORD=wiki123 -d mysql

mysql-clean:
	docker stop marytts-mysql
	docker rm -v marytts-mysql

github:
	 git clone https://github.com/techiaith/marytts.git
	 cd marytts && git checkout branch marytts-lang-cy
