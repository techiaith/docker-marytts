# Defnyddio eich lleisiau Cymraeg ar y Raspberry Pi

Mae modd gosod llais testun-i-leferydd Cymraeg MaryTTS parod ar y Raspberry Pi. 

Bydd angen i chi osod Docker yn gyntaf. Ewch i https://www.raspberrypi.org/blog/docker-comes-to-raspberry-pi/
am cyfarwyddiadau.

Ar ôl chi llwytho adnoddau docker-marytts i lawr gyda git:

`$ git clone https://github.com/techiaith/docker-marytts.git`

Defnyddiwch yn syth:

` $ cd docker-marytts/raspberrypi`

` $ cp *file ..`

Yna rhedwch:

`$ make` 


Copiwch eich ffeiliau `voice-<enw eich llais>-5.2.zip` a `voice-<enw eich llais>-5.2-component.xml` 
i'r cyfeiriadur `voice-building` ac yna rhedwch

`make run` 

i greu'r amgylchedd docker-marytts. 

Yna

`$ cd voice-building`

`$ voice-install.sh <enw eich llais>`

I gychwyn y llais, teipiwch:

`$ ~/target/marytts-5.2/bin/marytts-server`

Bydd gwefan darparu'r llais yn cychwyn ac ar gael ar y rhwydwaith o borth 59125 
eich Raspberry Pi. 

h.y. os agorwch chi porwr ar eich Pi, a mynd at 

http://localhost:59125 

bydd dudalen flaen MaryTTS yn ymddangos gyda'ch llais fel y dewis rhagosodedig.

Os nad oes modd rhedeg porwr (e.e. rydych chi'n defnyddio'r llinell gorchymun yn 
unig), yna mae modd profi'r llais drwy CURL: (*newidiwch <enw eich llais> o fewn 
y cyfeiriad)

`$ curl -v "http://localhost:59125/process?VOICE=<enw eich llais>&INPUT_TYPE=TEXT&OUTPUT_TYPE=AUDIO&INPUT_TEXT=dyma%20llais%20meri%20ti%20ti%20ti%20es%20cymraeg%20ar%20y%20rasperi%20pai&LOCALE=cy&AUDIO=WAVE_FILE" > llaisnewydd.wav`

`$ aplay llaisnewydd.wav`

