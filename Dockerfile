FROM ubuntu:14.04
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update \
	&& apt-get install -y openjdk-7-jdk maven git curl wget zip python3-mysql.connect

RUN export uid=1000 gid=1000 && \
	mkdir -p /home/marytts && \
	echo "marytts:x:${uid}:${gid}:Developer,,,:/home/marytts:/bin/bash" >> /etc/passwd && \
	echo "marytts:x:${uid}:" >> /etc/group && \
	echo "marytts ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/marytts && \
	chmod 0440 /etc/sudoers.d/marytts && \
	chown ${uid}:${gid} -R /home/marytts

USER marytts

ENV PATH="/home/marytts/target/marytts-builder-5.2/bin:${PATH}"
ENV HOME="/home/marytts"

WORKDIR /home/marytts

EXPOSE 59125

