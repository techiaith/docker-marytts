# Docker MaryTTS 

## Cyn cychwyn arni..

`$ make github`

`$ make mysql`


## Cychwyn arni...
Mae'r project yn defnyddio'r HTK i gynhyrchu modelau acwstig. Mae rhaid i chi gofrestru ar wefan http://htk.eng.cam.ac.uk, er mwyn derbyn enw defnyddiwr a chyfrinair er mwyn llwytho'r cod ffynhonnell i lawr. Mae modd llwytho'r cod i lawr fel hyn:

`$ wget --user <eich enw defnyddiwr HTK> --ask-password http://htk.eng.cam.ac.uk/ftp/software/HTK-3.4.1.tar.gz`

`$ wget --user <eich enw defnyddiwr HTK> --ask-password http://htk.eng.cam.ac.uk/ftp/software/HTK-samples-3.4.1.tar.gz`


Bydd yn gofyn am eich cyfrinair yn y man.

Bydd ddwy ffeil, HTK-3.4.1.tar.gz a HTK-samples-3.4.1.tar.gz yn bodoli o fewn y cyfeiriadur


`$ make`

`$ make run`

Bydd yr amgylchedd Docker yn cychwyn:




## Casglu testun ar gyfer sgriptiau

### O Wicipedia Cymraeg

`$ cd /home/marytts/texts/wici`

`$ create_database_docker.sh wkdb.conf`

`$ wkdb_collect.sh wkdb.conf`


### O ffynhonnell amgen...
Os oes gennych chi eisoes gasgliad o destunau amgen a glan eisoes yna :

`$ cd /home/marytts/texts/alt`

Mae modd estyn testun corpws Cofnod y Cynulliad o'r Porth Technolegau Iaith drwy:

`$ create_database_docker.sh wkdb.conf`

`$ getcorpustext_cy.sh -n CofnodYCynulliad`

`$ alt-cleantext-import.sh wkdb.conf alt-cleantext/CofnodYCynulliad/CofnodYCynulliad.cy`


## Cynhyrchu sgriptiau recordio

Oddi fewn texts/wici neu texts/alt, defnyddiwch:

`$ wkdb_featuremaker.sh wkdb.conf`

`$ wkdb_database_selector.sh wkdb.conf`

`$ selectedtext-dbexport.sh wkdb.conf`

Rydych yn barod nawr i reocrdio eich lais er mwyn creu system testun-i-leferydd eich hunain


## Recordio llais..

Rhaid dod allan o'r amgylchedd Docker er mwyn recordio. Os rydych chi wedi dilyn y camau uchod rhaid nawr dod
allan o'r amgylchedd Docker trwy: 

$ exit

Ewch i voice-builder

$ cd voice-builder/recorder

Fe welwch ffeil 'Prompts.py' ac ffolder o'r enw 'audio', yn ogystal a ddau ffeil cod Python. 
Er mwyn sicrhau bod holl cydrannau Python yn bodoli ar eich cyfrifiadur, defnyddiwch:

$ sudo pip install -r requirements.txt

Yna, 

$ python Record-Prompts-GUI.py


## Cynhyrchu llais testun i leferydd
Creu ffolder ar gyfer y llais newydd o dan ../voice-builder/. Gallwch rhoi unrhyw enw iddo. Yma rydyn yn dewis 'Macsen'

`$ mkdir -p voice-builder/macsen`


