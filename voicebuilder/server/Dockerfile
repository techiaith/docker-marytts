ARG MARYTTS_CY_VERSION
FROM techiaith/marytts-voicebuild:${MARYTTS_CY_VERSION}

RUN apt-get update \
	&& apt-get install -y libpq-dev supervisor python3-dev rabbitmq-server \
	&& rm -rf /var/lib/apt/lists/*

# Install voice-builder-api
ENV MARYTTS_VOICEBUILDER_API="${MARYTTS_HOME}/voice-builder-api"

ADD cherrypy ${MARYTTS_VOICEBUILDER_API}

WORKDIR ${MARYTTS_VOICEBUILDER_API}

RUN pip3 install -r requirements.txt \
	&& mkdir -p /var/log/gunicorn \
	&& mkdir -p /var/log/celery \
	&& touch /var/log/gunicorn/voice-builder-api.error.log

EXPOSE 8008 

CMD ["/bin/bash", "-c", "${MARYTTS_VOICEBUILDER_API}/start.sh"]
