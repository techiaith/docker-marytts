#!/bin/bash
cd ~/
wget https://www.ffmpeg.org/releases/ffmpeg-4.3.tar.gz
tar -xzf ffmpeg-4.3.tar.gz
cd ffmpeg-4.3
./configure --enable-gpl --enable-libmp3lame --enable-decoder=mjpeg,png --enable-encoder=png
make
sudo make install
ffmpeg
exit 0
