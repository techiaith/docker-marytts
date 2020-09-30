FROM techiaith/marytts:20.10

RUN apt-get update \
	&&  curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
	&&  apt-get install -y python3-mysql.connect mysql-client \
   	  			build-essential speech-tools praat tclsh libsnack2 libffi-dev \
				gcc-multilib libx11-dev:i386 zlib1g-dev libtool autotools-dev automake \
				sox alsa-utils pulseaudio audacity vim sudo git-lfs \
	&& git lfs install \
	&& rm -rf /var/lib/apt/lists/*


# Install basic NLP components. 
RUN pip3 install --upgrade pip && \
    pip3 install cld2-cffi wget praatio praat-parselmouth pandas webrtcvad


# Install and verify HTK
ADD HTK-3.4.1.tar.gz /usr/local/src
ADD HTK-samples-3.4.1.tar.gz /usr/local/src/htk/


WORKDIR /usr/local/src/htk
RUN ./configure \
	&& find . -type f -name Makefile -exec sed -i.bak 's/ \+ /\t/g' {} \; \
	&& make all \
	&& make install


RUN perl -i -pe 'y|\r||d' /usr/local/src/htk/samples/RMHTK/perl_scripts/*.prl

WORKDIR /usr/local/src/htk/samples/HTKDemo
RUN mkdir -p proto test hmms/hmm.0 hmms/hmm.1 hmms/hmm.2 hmms/tmp  \
 	&& ./runDemo configs/monPlainM1S1.dcf

# Add and Install MaryTTS
ADD templates ${MARYTTS_HOME}/voicebuilder/templates
ADD scripts ${MARYTTS_HOME}/voicebuilder/scripts

ENV PATH="${MARYTTS_HOME}/voicebuilder/scripts:${PATH}"

WORKDIR ${MARYTTS_HOME}/voicebuilder

# Running GUI apps with Docker : http://fabiorehm.com/blog/2014/09/11/running-gui-apps-with-docker
RUN export uid=1000 gid=1000 && \
	mkdir -p /home/marytts && \
	echo "marytts:x:${uid}:${gid}:MaryTTS,,,:/home/marytts:/bin/bash" >> /etc/passwd && \ 
	echo "marytts:x:${uid}:" >> /etc/group && \
	echo "marytts ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/marytts && \ 
	chmod 0440 /etc/sudoers.d/marytts && \
	chown ${uid}:${gid} -R /home/marytts

EXPOSE 59125

