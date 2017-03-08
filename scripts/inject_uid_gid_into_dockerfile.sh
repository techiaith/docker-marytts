#!/bin/bash

uid="$(id -u)"
gid="$(id -g)"

sed -i -- "s/UID/${uid}/g" Dockerfile
sed -i -- "s/GID/${gid}/g" Dockerfile
