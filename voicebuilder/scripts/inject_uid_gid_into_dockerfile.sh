#!/bin/bash

uid="$(id -u)"
gid="$(id -g)"

new_dockerfile_line="RUN export uid=${uid} gid=${gid} \&\& \\\\"
echo ${new_dockerfile_line}

sed -i -- "s/.*export uid=.*/deletedline/" Dockerfile
sed -i -- "s/deletedline.*/${new_dockerfile_line}/" Dockerfile 

