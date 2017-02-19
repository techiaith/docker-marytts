FROM ubuntu:14.04
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update \
	&& apt-get install -y openjdk-7-jdk maven git curl wget zip mysql-client

RUN mkdir -p /opt/marytts

WORKDIR /opt/marytts

ENV PATH="/opt/marytts/target/marytts-builder-5.2/bin:${PATH}"

EXPOSE 59125

