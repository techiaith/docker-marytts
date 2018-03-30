#!/bin/bash
echo "Starting rabbitmq-server"
service rabbitmq-server start

echo "Starting Celery Task Scheduler..."
supervisord -c supervisord/celery.conf

echo "Starting CherryPy..."
supervisord -c supervisord/cherrypy.conf

sleep infinity
