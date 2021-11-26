ARG MARYTTS_CY_VERSION
FROM techiaith/marytts:${MARYTTS_CY_VERSION}

RUN apt-get update \
 && apt-get install -y libpq-dev lame supervisor python3-dev \
 && rm -rf /var/lib/apt/lists/*

ADD cherrypy /opt/marytts-server
ADD cherrypy/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /opt/marytts-server

RUN pip3 install --upgrade pip
RUN python3 -m pip install -r requirements.txt 

EXPOSE 8008

CMD ["/usr/bin/supervisord"]
