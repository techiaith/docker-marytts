# docker-marytts

Yma ceir adnoddau ar gyfer rhedeg a ddatblygu testun-i-leferydd Cymraeg eich hunain yn hwylus iawn gan ddefnyddio MaryTTS a Docker*. 

## Dewisiadau defnyddio

Y dewisiadau defnyddio ar gyfer docker-marytts yw:

<br/>

### Defnyddio llais testun-i-leferydd o'r Porth Technolegau Iaith

Mae'r Uned Technolegau Iaith wedi defnyddio recordiadau o [Corpws WISPR](https://git.techiaith.bangor.ac.uk/Data-Porth-Technolegau-Iaith/Corpws-WISPR) i greu, gyda MaryTTS, llais naturiol gogleddol gwrywaidd. Mae modd arbrofi gyda'r llais ar wefan y Porth Technolegau Iaith (http://techiaith.cymru/lleferydd/testun-i-leferydd/) a'i defnyddio o fewn wasanaeth API ar-lein (https://github.com/PorthTechnolegauIaith/marytts/tree/master/doc/)

Os hoffwch chi ei defnyddio'n lleol ar eich cyfrifiadur eich hunain, yna defnyddiwch ar gyfrifiadur Linux neu Mac OS X:

`$ git clone https://github.com/techiaith/docker-marytts.git`

Ac yna:

`$ cd docker-marytts`

`$ make github`

`$ make `

`$ make runtime`

Bydd hyn yn cychwyn amgylchedd Docker lle mae modd llwytho'r llais i lawr a dechrau gweinydd lleferydd MaryTTS:

`root@9dcf4f9f904b:~# voice-download.sh wispr`

`root@9dcf4f9f904b:~# ./target/marytts-5.2/bin/marytts-server `

Mae modd dod allan o'r amgylchedd gan adael y gweinydd i redeg drwy bwyso CTRL-P ac yna CTRL-Q

Yna agorwch borwr ac ewch i `http://localhost:59125` i arbrofi rhagor.

<br/>

### Datblygu llais testun-i-lefrydd eich hunain

Mae modd defnyddio'r adnoddau MaryTTS hyn i greu lleisiau synthetig Cymraeg eich hunain. 

Dyma engreifftiau o'r leisiau o'r rhai aelodau Uned Technolegau Iaith sydd wedi'i trosi i lais synthetig gyda'r adnoddau hyn:

 - [Gwryw](http://techiaith.cymru/wp-content/uploads/2017/03/MaryTTS-CY-1.wav)

 - [Benyw](http://techiaith.cymru/wp-content/uploads/2017/03/MaryTTS-CY-2.wav)

Bydd angen defnyddio'r meddalwedd i recordio unigolyn yn darllen sgript recordio arbennig. Mae modd i chi hefyd cynhyrchu sgript recordio eich hunain er mwyn cynhyrchu lleisiau gorau ar gyfer parthau penodol.


#### Cychwyn arni

Er mwyn cychwyn arni i cynhyrchu lleisiau eich hunain, llwythwch yr adnoddau i lawr drwy ddefnyddio git:

`$ git clone https://github.com/techiaith/docker-marytts.git`

Ac yna:

`$ cd docker-marytts`

`$ make github`

`$ make mysql`

Mae'r project yn ogystal yn defnyddio'r HTK i gynhyrchu modelau acwstig. Mae rhaid i chi gofrestru ar wefan http://htk.eng.cam.ac.uk, er mwyn derbyn enw defnyddiwr a chyfrinair ar gyfer caniatáu llwytho cod ffynhonnell i lawr. Wedi i chi cael eich manylion, mae modd llwytho'r HTK i lawr fel hyn:

`$ wget --user <eich enw defnyddiwr HTK> --ask-password http://htk.eng.cam.ac.uk/ftp/software/HTK-3.4.1.tar.gz`

`$ wget --user <eich enw defnyddiwr HTK> --ask-password http://htk.eng.cam.ac.uk/ftp/software/HTK-samples-3.4.1.tar.gz`


Bydd yn gofyn am eich cyfrinair yn y man.

Bydd ddwy ffeil, `HTK-3.4.1.tar.gz` a `HTK-samples-3.4.1.tar.gz` yn bodoli o fewn y cyfeiriadur `docker-marytts`

Defnyddiwch y ddau orchymyn canlynol er mwyn adeiladu'r amgylchedd Mary TTS ar eich cyfrifiadur:

`$ make`

`$ make run`

Bydd yr amgylchedd Docker yn cychwyn.

Mae'r camau nesaf yn dibynol ar beth hoffwch chi ei gyflawni:

 * [paratoi sgript recordio o ffynhonnell testun penodol](#creusgript)
<br/>
 * [recordio unigolyn i gynhyrchu llais testun-i-leferydd newydd](#recordiosgript)
<br/>
 * [gosod a rhedeg eich llais newydd](#defnyddiollais) 


---

##### <a name="creusgript"></a> Paratoi Sgriptiau Recordio

Bydd angen gorff swmpus o destun er mwyn cael ddigon o ddewis ar gyfer brawddegau addas ar gyfer sgript recordio. Y ffynonellau bosib yw:

###### Wicipedia Cymraeg fel ffynhonnell testun

Defnyddiwch y gorchmynion canlynol:

`$ cd /home/marytts/texts/wici`

`$ create_database_docker.sh wkdb.conf`

`$ wkdb_collect.sh wkdb.conf`


###### Ffynhonnell testun amgen...

Os oes gennych chi gasgliad o destunau amgen a glan eisoes yna :

`$ cd /home/marytts/texts/alt`

`$ create_database_docker.sh wkdb.conf`

Mae modd estyn enghraifft o destun o ffynhonnell amgen, fel Cofnod y Cynulliad, 
o'r Porth Technolegau Iaith drwy defnyddio:

`$ getcorpustext_cy.sh -n CofnodYCynulliad`

Bydd angen mewnforio'r pwy bynnag testun i amgylchedd MaryTTS trwy ddefnyddio:

`$ alt-cleantext-import.sh wkdb.conf alt-cleantext/CofnodYCynulliad/CofnodYCynulliad.cy`


###### Cynhyrchu sgriptiau recordio

Ar ôl casglu testunau, ewch i'ch cyfeiriadur texts/wici neu texts/alt ac yna 
defnyddiwch:

`$ wkdb_featuremaker.sh wkdb.conf`

`$ wkdb_database_selector.sh wkdb.conf`

`$ selectedtext-dbexport.sh wkdb.conf`

Mae hyn yn cynhyrchu sgript recordio o'r testunau lle mae'r wybodaeth am ynganu'r 
Gymraeg wedi'i ddefnyddio i sicrhau bod ddigon o enghreifftiau o bob ffonem ac 
elfen sain eraill y Gymraeg wedi eu cynnwys.

Rydych yn barod nawr i recordio eich llais er mwyn creu system testun-i-leferydd 
eich hunain fel y disgrifir yn y camau nesaf.

<br/>

---

##### <a name="recordiosgript"></a> Recordio a chynhyrchu llais testun-i-leferydd newydd

###### Recordio

Mae sgript eisoes, neu'r un rydych wedi cynhyrchu gyda sgriptiau docker-marytts
wedi ei chadw yn:

https://github.com/techiaith/docker-marytts/blob/master/voice-builder/recorder/Prompts.py

Mae rhaid recordio'r promtiau hyn **tu allan i'r amgylchedd Docker**. 

Felly o fewn eich amgylchedd linell gorchymyn arferol eich cyfrifiadur, ewch i 
cyfeiriadur `docker-marytts/voice-builder/recorder`

`$ cd voice-builder/recorder`

Fe welwch ffeil 'Prompts.py' yn ogystal a ddau ffeil cod Python. Er mwyn sicrhau 
bod holl cydrannau Python yn bodoli ar eich cyfrifiadur, defnyddiwch:

`$ sudo apt install audacity portaudio19-dev python3-pip`

`$ sudo pip3 install -r requirements.txt`

Ac yna, 

`$ python3 Record-Prompts-GUI.py`

Bydd rhaglen fach syml ymddangos ar gyfer recordio pob prompt yn y sgript. 


###### Cynhyrchu llais testun-i-leferydd

Ar ôl cwblhau'r recordio, defnyddiwch y gorchymyn canlynol i ddynodi enw i'ch 
llais newydd. Yma rydyn yn dewis 'macsen'

`$ ./init-voice-build.sh macsen`

Mae gweddill y camau angen mynd yn ôl i amgylchedd MaryTTS o fewn Docker. 

Felly:

`$ docker exec -it marytts bash`

`$ cd /home/marytts/voice-builder/macsen`

A chychwyn y rhaglen glanhau a gwella ansawdd eich recordiadau

`$ audio_converter_GUI.sh`

Dewisiwch y ffolder:

 - `/home/marytts/voice-builder/macsen/recordings`

ar gyfer 'Input Wave directory', ac yna:

 - `/home/marytts/voice-builder/macsen/wav`

ar gyfer 'Output Wave directory (*mae'n bosib creu'r ffolder 'wav' o fewn y GUI 
os nad yw'n bodoli eisoes*)

Ar ol i'r broses llnau a gwella'r recordiadau cwblhau, defnyddiwch yr orchymun 
canlynol:

`$ voice-import-cy.sh`

Bydd hyn yn achosi i raglen GUI newydd ymddangos, gyda chyfres o gamau sydd eu 
hangen ar gyfer creu testun i leferydd 'unit selection'. 

Ticiwch bob un yn eu tro, gan droi pob un rhes yn wyrdd. 

Caewch y rhaglen ar ôl cwblhau 'Compile voice', a bydd ffeiliau newydd sy'n 
pecynnu'r llais newydd ar gael yn 

`$ /home/marytts/voice-builder/macsen/mary/voice-macsen/target`

Yn benodol:

 - `voice-macsen-5.2-component.xml`
 - `voice-macsen-5.2.zip`

--- 

#### <a name="defnyddiollais"></a> Defnyddio llais newydd 

Os oes gennych chi'r ffeiliau `voice-macsen-5.2-component.xml` a 
`voice-macsen-5.2.zip` ar gyfer llais newydd yna defnyddiwch y gorchymyn canlynol 
er mwyn eu hychwanegu i'r weinydd MaryTTS o fewn eich amgylchedd docker-marytts:

`$ voice-install-cy.sh macsen`

Defnyddiwch y gorchymyn canlynol i gychwyn gweinydd MaryTTS a'ch llais newydd:

`$ cd /home/marytts`

`$ ./target/marytts-5.2/bin/marytts-server`

Agorwch borwr ac ewch i `http://localhost:59125` i brofi a mwynhau eich llais 
synthetig Cymraeg newydd.


