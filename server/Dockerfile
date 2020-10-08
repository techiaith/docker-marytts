ARG MARYTTS_CY_VERSION
FROM techiaith/marytts:${MARYTTS_CY_VERSION}

RUN apt-get update \
 && apt-get install -y \
	libpq-dev lame supervisor python python-pip python-dev \
 && rm -rf /var/lib/apt/lists/*

ADD cherrypy /opt/marytts-server
ADD cherrypy/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /opt/marytts-server

RUN pip install -r requirements.txt 

RUN mkdir -p /var/log/gunicorn \
 && touch /var/log/gunicorn/marytts-api.error.log

EXPOSE 8008

CMD ["/usr/bin/supervisord"]

