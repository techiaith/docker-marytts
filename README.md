# docker-marytts

Yma ceir testun-i-leferydd Cymraeg a ddwyieithog gan ddefnyddio MaryTTS a docker. 

Ewch i'r ddogfennaeth yn y ffolder [`voicebuilder`](voicebuilder/README.md) am sgriptiau defnyddir i adeiladu lleisiau Cymraeg a ddwyieithog.

<br/>


## Lleisiau testun-i-leferydd o'r Porth Technolegau Iaith

Mae Uned Technolegau Iaith, Prifysgol Bangor eisoes wedi creu lleisiau destun-i-leferydd Cymraeg sydd wedi eu creu gyda ddau set data agored: 

1 - [Corpws WISPR](https://git.techiaith.bangor.ac.uk/Data-Porth-Technolegau-Iaith/Corpws-WISPR) 

2 - [Corpws Talentau Llais]()

O ganlyniad, mae lleisiau gwrywaidd a benywaidd gydag acenion gogleddol ar gael sy'n swnion mor naturiol â phosib. 

Os hoffwch chi eu gosod a'u rhedeg ar weinydd neu gyfrifiadur eich hunain, yna defnyddiwch y gorchmynion canlynol:

`$ git clone https://github.com/techiaith/docker-marytts.git`

Ac yna:

`$ cd docker-marytts`

`$ make `

`$ cd server`

`$ make`

`$ make run`

Bydd hyn yn cychwyn gweinydd testun-i-leferydd gyda'r llais Cymraeg (wispr-cy-male-unitselection-general) yn barod i'w ddefnyddio. 

Agorwch borwr ac ewch i [http://localhost:52010](http://localhost:52010) i'w glywed yn ynganu eich testunau neu defnyddiwch y gorchymyn CURL:

 $ curl -o sound.wav "http://localhost:52010/process?INPUT_TEXT=Helo+pawb&INPUT_TYPE=TEXT&OUTPUT_TYPE=AUDIO&AUDIO=WAVE&VOICE=wispr&LOCALE=cy"


