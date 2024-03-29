FROM ubuntu:16.04

RUN dpkg --add-architecture i386

RUN apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y default-jdk vim git curl wget zip locales maven  \
	   software-properties-common build-essential cmake libssl-dev libboost-all-dev zlib1g-dev libffi-dev \
	&& rm -rf /var/lib/apt/lists/*

# Upgrade to Python3.7
RUN wget -c https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tar.xz && \
    tar xf Python-3.7.4.tar.xz && \
    cd Python-3.7.4 && ./configure -q && make && make install && \
    apt update && \
    apt install -y python3 python3-dev python3-setuptools python3-pip

RUN python3 -m pip install --upgrade pip 

# Set the locale
RUN locale-gen cy_GB.UTF-8
ENV LANG cy_GB.UTF-8
ENV LANGUAGE cy_GB:en
ENV LC_ALL cy_GB.UTF-8

RUN pip3 install wget py-marytts

# Add and Install MaryTTS
ARG BUILDARG_MARYTTS_CY_VERSION
ENV MARYTTS_CY_VERSION=${BUILDARG_MARYTTS_CY_VERSION}

ENV MARYTTS_VERSION="5.2"
ENV MARYTTS_HOME="/opt/marytts"
ENV MARYTTS_VOICES_HOME="/voices"
ENV MARYTTS_CY_HOME="${MARYTTS_HOME}/marytts-languages/marytts-lang-cy"

ADD marytts ${MARYTTS_HOME}

ENV PATH="${MARYTTS_HOME}/target/marytts-builder-${MARYTTS_VERSION}/bin:${MARYTTS_CY_HOME}/bin:${PATH}"
ENV PYTHONPATH "${PYTHONPATH}:${MARYTTS_HOME}/marytts-languages/marytts-lang-cy/bin/python"

WORKDIR ${MARYTTS_HOME}

RUN update-marytts-server-cy.sh

RUN voice-download.sh wispr \
 && voice-download.sh benyw-gogledd

EXPOSE 59125

