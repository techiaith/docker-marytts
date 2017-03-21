# MaryTTS o fewn Docker ar y Raspberry Pi

Dyma ffeiliau sydd yn eich galluogi defnyddio'r feddalwedd i ddarparu eich lais MaryTTS Cymraeg ar y RaspberryPi. 
@todo - er mwyn cael llais lleol i Macsen ayb


Bydd angen i chi osod Docker yn gyntaf:

 - gweler : https://www.raspberrypi.org/blog/docker-comes-to-raspberry-pi/

Copiwch y ffeil Dockerfile a Makefile i'r cyfeiriadur top, ac yna rhedeg `make` 

Copiwch eich ffeiliau voice-<enw eich llais>-5.2.zip a voice-<enw eich llais>-5.2-component.xml i'ch `voice-building`.

Yna rhedwch `make run` i greu'r amgylchedd MaryTTS. 

Yna

$ cd voice-building

$ voice-install.sh <enw eich llais>

I gychwyn y llais, teipiwch:

$ ~/target/marytts-5.2/bin/marytts-server

Bydd gwefan darparu'r llais yn cychwyn ac ar gael ar y rhwydwaith o borth 59125 eich Raspberry Pi. 

h.y. os agorwch chi porwr ar eich Pi, a mynd at http://localhost:59125 bydd dudalen flaen MaryTTS yn ymddangos gyda'ch llais fel y prif ddewis rhagosodedig.

Os nad oes modd rhedeg porwr (e.e. rydych chi'n defnyddio'r llinell gorchymun yn unig), yna mae modd profi'r llais drwy CURL: 

$ curl -v "http://localhost:59125/process?INPUT_TYPE=TEXT&OUTPUT_TYPE=AUDIO&INPUT_TEXT=dyma%20llais%20meri%20ti%20ti%20ti%20es%20cymraeg%20ar%20y%20rasperi%20pai&LOCALE=cy&VOICE=<enw eich llais&AUDIO=WAVE_FILE" > llaisnewydd.wav
$ aplay llaisnewydd.wav

