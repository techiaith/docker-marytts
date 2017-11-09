Dethol 400 gair o lecsicon ynganu Cymraeg y Porth Technolegau Iaith 400 sydd yn 
ymdrin gorau o ffoneteg y Gymraeg o fewn deitlau Wicipedia Cymraeg.

Cynhyrchir y ffeiliau canlynol o bwys:

1. lexicon.cy - geiriau o'r lecsicon ynganu sy'n bodoli o fewn teitlau erthyglau Wicipedia
2. lexicon_cld2.cy - geiriau Cymraeg (yn ôl cld2) sydd ddim yn bodoli yn y lecsicon ynganu
3. lexicon.xx - geiriau ieithoedd eraill (eto, yn ôl cld2)
4. selected.log - y 400 air gyda'r ymdriniaeth gorau o ffoneteg Cymraeg teitlau Wicipedia
 

I'w greu defnyddiwch:

`$ python3 CreateLexiconSubset.py`

`$ create-database-docker.sh wkdb.conf`

`$ alt-cleantext-import.sh wkdb.conf lexicon.cy`

`$ wkdb_featuremaker.sh wkdb.conf`

`$ wkdb_database_selector.sh wkdb.conf`


*Diolch i Robin Owain am ddarparu'r rhestr deitlau Wicipedia Cymraeg*
