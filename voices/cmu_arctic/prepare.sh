#!/bin/bash

wget http://www.speech.cs.cmu.edu/cmu_arctic/packed/cmu_us_slt_arctic-0.95-release.tar.bz2
bzip2 -d cmu_us_slt_arctic-0.95-release.tar.bz2
tar xvf cmu_us_slt_arctic-0.95-release.tar
rm cmu_us_slt_arctic-0.95-release.tar
ln -s cmu_us_slt_arctic/wav wav
cp cmu_us_slt_arctic/etc/txt.done.data txt.done.data
