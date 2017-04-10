# Docker MaryTTS 

Yma ceir adnoddau ar gyfer datblygu testun-i-leferydd Cymraeg gan ddefnyddio Mary TTS yn hwylus iawn gyda'r amgylchedd Docker. 

Dyma engreifftiau o leisiau dau aelod o'r techiaith wedi'i trosi i lais cyfrifiadurol:

 - [Gwryw](http://techiaith.cymru/wp-content/uploads/2017/03/MaryTTS-CY-1.wav)

 - [Benyw](http://techiaith.cymru/wp-content/uploads/2017/03/MaryTTS-CY-2.wav)


Mae modd llwytho i lawr Docker ar gyfer eich cyfrifiadur Mac neu Linux o'r dudalen we canlynol:

https://www.docker.com/community-edition

Llwythwch yr adnoddau i lawr drwy ddefnyddio git:

`$ git clone https://github.com/techiaith/docker-marytts.git`


## Cyn cychwyn arni..

Rhaid cael adnoddau a meddalwedd pellach wedi eu llwytho a'u osod ar eich cyfrifiadur. Mae rhedeg y ddau orchymyn `make` canlynol oddi fewn y cyfeiriadur `docker-marytts`, yn eu osod ar eich rhan :

`$ cd docker-marytts`

`$ make github`

`$ make mysql`

Mae'r project yn ogystal yn defnyddio'r HTK i gynhyrchu modelau acwstig. Mae rhaid i chi gofrestru ar wefan http://htk.eng.cam.ac.uk, er mwyn derbyn enw defnyddiwr a chyfrinair ar gyfer caniatáu llwytho cod ffynhonnell i lawr. Wedi i chi cael eich manylion, mae modd llwytho'r HTK i lawr fel hyn:

`$ wget --user <eich enw defnyddiwr HTK> --ask-password http://htk.eng.cam.ac.uk/ftp/software/HTK-3.4.1.tar.gz`

`$ wget --user <eich enw defnyddiwr HTK> --ask-password http://htk.eng.cam.ac.uk/ftp/software/HTK-samples-3.4.1.tar.gz`


Bydd yn gofyn am eich cyfrinair yn y man.

Bydd ddwy ffeil, HTK-3.4.1.tar.gz a HTK-samples-3.4.1.tar.gz yn bodoli o fewn y cyfeiriadur `docker-marytts`

Defnyddiwch y ddau orchymyn canlynol er mwyn adeiladu'r amgylched Mary TTS ar eich cyfrifiadur:

`$ make`

`$ make run`

Bydd yr amgylchedd Docker yn cychwyn.


## Dewisiadau defnyddio

Mae'r camau ar gyfer creu llais testun-i-leferydd newydd gyda MaryTTS yn cynnwys :

 1. casglu testunau o gasgliadau eich hunain ac/neu Wicipedia
 2. defnyddio'r testunau i gynhyrchu sgript recordio
 3. recordio unigolyn yn darllen y sgript recordio i gyd
 4. cynhyrchu llais newydd o'r recordiadau
 5. gosod y llais newydd o fewn eich gosodiad  MaryTTS

Mae modd cychwyn o'r cam 3 gan fod sgriptiau eisoes o fewn yr adnoddau hyn ( gweler : https://github.com/techiaith/docker-marytts/blob/master/voice-builder/recorder/Prompts.py) . Ewch i'r adran 'Recordio llais..' isod i gamu dros y cyfarwyddiadau ynghylch darparu sgriptiau recordio eich hunain.


## Casglu testun ar gyfer sgriptiau

### O Wicipedia Cymraeg

`$ cd /home/marytts/texts/wici`

`$ create_database_docker.sh wkdb.conf`

`$ wkdb_collect.sh wkdb.conf`


### O ffynhonnell amgen...

Os oes gennych chi gasgliad o destunau amgen a glan eisoes yna :

`$ cd /home/marytts/texts/alt`

`$ create_database_docker.sh wkdb.conf`

Mae modd estyn enghraifft o destun o ffynhonnell amgen, fel Cofnod y Cynulliad, o'r Porth Technolegau Iaith drwy defnyddio:

`$ getcorpustext_cy.sh -n CofnodYCynulliad`

Bydd angen mewnforio'r pwy bynnag testun i amgylchedd MaryTTS trwy ddefnyddio:

`$ alt-cleantext-import.sh wkdb.conf alt-cleantext/CofnodYCynulliad/CofnodYCynulliad.cy`


## Cynhyrchu sgriptiau recordio

Ar ôl casglu testunau, ewch i'ch cyfeiriadur texts/wici neu texts/alt i ddefnyddio:

`$ wkdb_featuremaker.sh wkdb.conf`

`$ wkdb_database_selector.sh wkdb.conf`

`$ selectedtext-dbexport.sh wkdb.conf`

Mae hyn yn cynhyrchu sgript recordio o'r testunau lle mae'r wybodaeth am ynganu'r Gymraeg wedi'i ddefnyddio i sicrhau bod ddigon o enghreifftiau o bob ffonem ac elfennau sain eraill y Gymraeg wedi eu cynnwys.

Rydych yn barod nawr i recordio eich llais er mwyn creu system testun-i-leferydd eich hunain fel y disgrifir yn y camau nesaf.


## Recordio llais..

Mae rhaid recordio tu allan i'r amgylchedd Docker, felly bydd angen defnyddio'r gorchymyn canlynol i'w gadael:

`$ exit`

Ewch i cyfeiriadur `voice-builder/recorder`

`$ cd voice-builder/recorder`

Fe welwch ffeil 'Prompts.py' ac ffolder o'r enw 'audio', yn ogystal a ddau ffeil cod Python. Er mwyn sicrhau bod holl cydrannau Python yn bodoli ar eich cyfrifiadur, defnyddiwch:

`$ sudo pip install -r requirements.txt`

Ac yna, 

`$ python Record-Prompts-GUI.py`

bydd rhaglen fach syml ymddangos ar gyfer recordio pob prompt yn y sgript. 


## Cynhyrchu llais testun-i-leferydd

Ar ôl cwblhau'r recordio, defnyddiwch y gorchymyn canlynol i ddynodi enw i'ch llais newydd. Yma rydyn yn dewis 'macsen'

`$ ./init-voice-build.sh macsen`

Mae gweddill y camau angen mynd yn ôl i amgylchedd MaryTTS o fewn Docker. Felly:

`$ docker exec -it marytts bash`

`$ cd /home/marytts/voice-builder/macsen`

A chychwyn y rhaglen glanhau a gwella ansawdd eich recordiadau

`$ audio_converter_GUI.sh`

Dewis y ffolder:

 - `/home/marytts/voice-builder/macsen/recordings`

ar gyfer 'Input Wave directory', ac yna:

 - `/home/marytts/voice-builder/macsen/wav`

ar gyfer 'Output Wave directory (*mae'n bosib creu'r ffolder 'wav' o fewn y GUI os nad yw'n bodoli eisoes*)


Ar ol i'r broses llnau a gwella'r recordiadau cwblhau, defnyddiwch yr orchymun canlynol:

`$ voice-import-cy.sh`

Bydd hyn yn achosi i raglen GUI newydd ymddangos, gyda chyfres o gamau sydd eu hangen ar gyfer creu testun i leferydd
'unit selection'. 

Ticiwch bob un yn eu tro, gan droi pob un rhes yn wyrdd. 

Caewch y rhaglen ar ôl cwblhau 'Compile voice', a bydd ffeiliau newydd sy'n pecynnu'r llais newydd ar gael yn 

`$ /home/marytts/voice-builder/macsen/mary/voice-macsen/target`

Yn benodol:

 - `voice-macsen-5.2-component.xml`
 - `voice-macsen-5.2.zip`

Defnyddiwch y gorchymyn canlynol er mwyn gosod y ffeiliau hyn i mewn i weinydd MaryTTS:

`$ voice-install-cy.sh macsen`

Defnyddiwch y gorchymyn canlynol i gychwyn gweinydd MaryTTS a'ch llais newydd:

`$ cd /home/marytts`

`$ ./target/marytts-5.2/bin/marytts-server`

Agorwch borwr ac eich i `http://localhost:59125` i brofi a mwynhau eich llais synthetig Cymraeg newydd.





