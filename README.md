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

`$ cd /home/marytts`

`$ cd texts`



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


Creu ffolder ar gyfer y llais newydd o dan ../voices/

`$ mkdir -p ../voices/<enwllais>`

`$ ./selectedtext-dbexport.sh wkdb.conf ../voices/<enwllais>/Prompts.py`



## Recordio llais..



## Creu'r testun i leferydd..



