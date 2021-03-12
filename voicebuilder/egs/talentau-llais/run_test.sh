#!/bin/bash

rm -rf test_audio
mkdir -p test_audio/benyw-gogledd
mkdir -p test_audio/gwryw-gogledd

i=0
while read NAME
do
    it=`echo -ne "$NAME" | xxd -plain | tr -d '\n' | sed 's/\(..\)/%\1/g'`
    curl -o test_audio/benyw-gogledd/$i.wav "http://localhost:59136/process?INPUT_TEXT=$it&INPUT_TYPE=TEXT&OUTPUT_TYPE=AUDIO&AUDIO=WAVE&VOICE=benyw-gogledd&LOCALE=cy"
    curl -o test_audio/gwryw-gogledd/$i.wav "http://localhost:59136/process?INPUT_TEXT=$it&INPUT_TYPE=TEXT&OUTPUT_TYPE=AUDIO&AUDIO=WAVE&VOICE=gwryw-gogledd&LOCALE=cy"
    ((i=i+1))
done < testData/testLines.txt

rm test_audio.zip
zip -r test_audio.zip test_audio
