FROM resin/rpi-raspbian:jessie-20160831 
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update \
	&& apt-get install -y oracle-java7-jdk maven git curl wget zip python3-mysql.connect mysql-client \
						  build-essential speech-tools tcl libsnack2 \
						  libx11-dev zlib1g-dev libtool autotools-dev automake \
						  sox alsa-utils pulseaudio \
	&& rm -rf /var/lib/apt/lists/*


# Add and Install MaryTTS
ADD marytts /home/marytts

ENV PATH="/home/marytts/target/marytts-builder-5.2/bin:/home/marytts/marytts-languages/marytts-lang-cy/bin:${PATH}"
ENV HOME="/home/marytts"

# Running GUI apps with Docker : http://fabiorehm.com/blog/2014/09/11/running-gui-apps-with-docker
RUN export uid=1000 gid=1000 && \
	mkdir -p /home/marytts && \
	echo "marytts:x:${uid}:${gid}:MaryTTS,,,:/home/marytts:/bin/bash" >> /etc/passwd && \
	echo "marytts:x:${uid}:" >> /etc/group && \
	echo "marytts ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/marytts && \
	chmod 0440 /etc/sudoers.d/marytts && \
	chown ${uid}:${gid} -R /home/marytts

USER marytts
WORKDIR /home/marytts

#RUN mvn install
RUN update-marytts-server.sh

EXPOSE 59125

