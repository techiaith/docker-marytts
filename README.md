# Docker MaryTTS 

## Cychwyn arni..
$ make github

$ make mysql


Mae'r project yn defnyddio'r HTK i gynhyrchu modelau acwstig. Mae rhaid i chi gofrestru ar wefan http://htk.eng.cam.ac.uk, er mwyn derbyn enw defnyddiwr a chyfrinair er mwyn llwytho'r cod ffynhonnell i lawr. Mae modd llwytho'r cod i lawr fel hyn:

$ wget --user <eich enw defnyddiwr HTK> --ask-password http://htk.eng.cam.ac.uk/ftp/software/HTK-3.4.1.tar.gz

$ wget --user <eich enw defnyddiwr HTK> --ask-password http://htk.eng.cam.ac.uk/ftp/software/HTK-samples-3.4.1.tar.gz

Bydd yn gofyn am eich cyfrinair yn y man.

Bydd ddwy ffeil, HTK-3.4.1.tar.gz a HTK-samples-3.4.1.tar.gz yn bodoli o fewn y cyfeiriadur


$ make

$ make run

$ mvn install

$ cd marytts-languages/mary-lang-cy

$ ./update-marytts-server.sh



## Paratoi sgriptiau..

$ cd /home/marytts

$ cd wikidump

$ wkdb_collect.sh wkdb.conf

$ wkdb_featuremaker.sh wkdb.conf

$ wkdb_database_selector.sh wkdb.conf

$ cd /home/marytts/marytts-languages/marytts-lang-cy/

$ ./selectedtext-dbexport.sh /home/marytts/wikidump/wkdb.conf Prompts.py



## Paratoi sgriptiau o ffynhonnell amgen..



## Recordio llais..



## Creu testun i leferydd..



