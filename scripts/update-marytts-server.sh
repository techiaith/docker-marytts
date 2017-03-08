#!/bin/bash

MARYTTS_VERSION="5.2"

mvn install
cp -v target/marytts-lang-cy-${MARYTTS_VERSION}.jar ../../target/marytts-${MARYTTS_VERSION}/lib
cp -v target/marytts-lang-cy-${MARYTTS_VERSION}.jar ../../target/marytts-builder-${MARYTTS_VERSION}/lib
