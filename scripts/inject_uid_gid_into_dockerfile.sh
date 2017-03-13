#!/bin/bash

uid="$(id -u)"
gid="$(id -g)"

sed -i -- "s/export uid=.* gid=.* && \ /export uid=${uid} gid=${gid} && \ /g" Dockerfile

