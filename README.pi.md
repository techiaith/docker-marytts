# Defnyddio MaryTTS ar y Raspberry Pi 


Mae modd gosod llais testun-i-leferydd Cymraeg MaryTTS parod ar y Raspberry Pi. 

Bydd angen i chi osod Docker yn gyntaf. Ewch i https://www.raspberrypi.org/blog/docker-comes-to-raspberry-pi/
am cyfarwyddiadau.

Ar ôl chi llwytho adnoddau docker-marytts i lawr gyda git:

`$ git clone https://github.com/techiaith/docker-marytts.git`

Ewch i fewn i'r ffolder `docker-marytts' newydd:

`$ cd docker-marytts`

Gellir gweld cynnwys y ffolder drwy defnyddio'r orchymyn `ls`

```
pi@raspberrypi:~/src/techiaith/docker-marytts$ ls 
Dockerfile.pi       Dockerfile.runtimeapi  Dockerfile.voicebuildapi  Makefile.pi  marytts-api  README.pi.md    scripts  voicebuild-api.sh  voice-builder-api
Dockerfile.runtime  Dockerfile.voicebuild  Makefile                  marytts      README.md    runtime-api.sh  texts    voice-builder
```

I adeiladu MaryTTS i'r Raspberry Pi, rhedwch:

`$ make -f Makefile.pi` 



## Defnyddio llais Cymraeg eich hunain 

Copiwch eich ffeiliau `voice-<enw eich llais>-5.2.zip` a `voice-<enw eich llais>-5.2-component.xml` 
i'r cyfeiriadur `voice-building` ac yna rhedwch

`make run` 

Yna: 

`$ cd voice-building`

`$ voice-install.sh <enw eich llais>`

I gychwyn y llais, teipiwch:

`$ ~/target/marytts-5.2/bin/marytts-server`

Agorwch porwr ar eich Pi ac ewch i http://localhost:59125 

bydd dudalen we MaryTTS yn ymddangos gyda'ch llais fel y dewis rhagosodedig.

Os nad oes modd rhedeg porwr (e.e. rydych chi'n defnyddio'r llinell gorchymun yn 
unig), yna mae modd profi'r llais drwy CURL: (*newidiwch <enw eich llais> o fewn 
y cyfeiriad)

`$ curl -v "http://localhost:59125/process?VOICE=<enw eich llais>&INPUT_TYPE=TEXT&OUTPUT_TYPE=AUDIO&INPUT_TEXT=dyma%20llais%20meri%20ti%20ti%20ti%20es%20cymraeg%20ar%20y%20rasperi%20pai&LOCALE=cy&AUDIO=WAVE_FILE" > llaisnewydd.wav`

`$ aplay llaisnewydd.wav`

## Llwytho llais gan techiaith

Mae'r Uned Technolegau Iaith wedi creu llais Cymraeg ar gyfer MaryTTS sydd ar gael i chi defnyddio o fewn unrhyw broject ac/neu cynnyrch masnachol dan delerau hael ac am ddim.  

Yn gyntaf, rhedwch :

`make run`

Yna:

`$ voice-download.sh wispr`

'wispr' yw enw'r llais. Ar ol iddo gwblhau, teipiwch:

`$ ~/target/marytts-5.2/bin/marytts-server`

Ac yna ewch i http://localhost:59125 o fewn porwr. 


