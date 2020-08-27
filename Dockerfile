FROM ubuntu:16.04

RUN dpkg --add-architecture i386

RUN apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y default-jdk git curl wget zip locales maven  \
	   python3 python3-pip \
	&& rm -rf /var/lib/apt/lists/*

# Set the locale
RUN locale-gen cy_GB.UTF-8
ENV LANG cy_GB.UTF-8
ENV LANGUAGE cy_GB:en
ENV LC_ALL cy_GB.UTF-8

RUN pip3 install wget 

# Add and Install MaryTTS
ENV MARYTTS_VERSION="5.2"
ENV MARYTTS_HOME="/opt/marytts"
ENV MARYTTS_VOICES_HOME="/voices"
ENV MARYTTS_CY_HOME="${MARYTTS_HOME}/marytts-languages/marytts-lang-cy"

ADD marytts ${MARYTTS_HOME}

ENV PATH="${MARYTTS_HOME}/target/marytts-builder-${MARYTTS_VERSION}/bin:${MARYTTS_CY_HOME}/bin:${PATH}"

WORKDIR ${MARYTTS_HOME}

RUN update-marytts-server-cy.sh

EXPOSE 59125

