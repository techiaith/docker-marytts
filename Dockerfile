FROM ubuntu:14.04
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN dpkg --add-architecture i386

RUN locale-gen cy_GB.UTF-8
ENV LANG='cy_GB.UTF-8' LANGUAGE='cy_GB:cy' LC_ALL='cy_GB.UTF-8'

RUN apt-get update \
	&& apt-get install -y openjdk-7-jdk maven git curl wget zip python3-mysql.connect mysql-client \
						  build-essential speech-tools praat tclsh libsnack2 \
						  gcc-multilib libx11-dev:i386 zlib1g-dev libtool autotools-dev automake \
						  sox alsa-utils pulseaudio audacity \
	&& rm -rf /var/lib/apt/lists/*

# Install HTK
ADD HTK-3.4.1.tar.gz /usr/local/src
ADD HTK-samples-3.4.1.tar.gz /usr/local/src/htk/

WORKDIR /usr/local/src/htk

RUN ./configure
RUN make all
RUN make install

RUN perl -i -pe 'y|\r||d' /usr/local/src/htk/samples/RMHTK/perl_scripts/*.prl

WORKDIR /usr/local/src/htk/samples/HTKDemo
RUN mkdir -p proto test hmms/hmm.0 hmms/hmm.1 hmms/hmm.2 hmms/tmp 
RUN ./runDemo configs/monPlainM1S1.dcf


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

