# Creu lleisiau testun-i-leferydd eich hunain

Yma ceir adnoddau ar gyfer hyfforddi lleisiau testun i leferydd Cymraeg a ddwyieithog eich hunain. Er bod lleisiau ar gael gan uned technolegau iaith prifysgol Bangor, mae'n bosib eich bod eisio llais â hunaniaeth wahanol neu'n sy'n ynganu'n well o fewn parth penodol. 

Mae'r ffolder hwn yn cynnwys sawl 'rysait' rydym yn defnyddio ar gyfer cynhyrchu sgriptiau recordio ac i hyfforddi leisiau MaryTTS newydd. 

Gweler:

 - `egs/wispr` - sgriptiau i lwytho lawr data recordiadau Corpws WISPR a hyfforddi.
 - `egs/lleisiwr` - sgriptiau hyfforddi gyda recordiadau gwefan https://lleisiwr.techiaith.cymru
 - `egs/commonvoice` - sgriptiau sy'n cynhyrchu sgriptiau recordio gyda brawddegau CC-0 CommonVoice Cymraeg a Saesneg. 
 - `egs/talentau-llais` - sgriptiau i lwytho lawr recordiadau gan dalentau llais ac yna hyfforddi. 

Y dull mwya hwylus, sydd dim angen gosod unrhyw feddalwedd yn lleol ar eich cyfrifiadur yw defnyddio'r gwasanaeth Lleisiwr, sef gwefan bancio lleisiau. Gellir defnyddio'r wefan i recordio brawddegau wedi'i dewis gan yr uned technolegau iaith ac yna clicio botwm i gynhyrchu llais TTS ddwyieithog Cymraeg a Saesneg newydd ac yna i'w ddefnyddio gyda blwch testun neu drwy API. Ewch i https://lleisiwr.techiaith.cymru neu cysylltwch â techiaith@bangor.ac.uk. 

## HTK

Mae'r meddalwedd adeiladu lleisiau angen cod y llyfrgell HTK i gynhyrchu modelau acwstig. Cofrestrwch ar wefan http://htk.eng.cam.ac.uk, creu enw defnyddiwr a chyfrinair, ac yna defnyddiwch y gorchmynion canlynol i lwytho'r cod i lawr:

`$ wget --user <eich enw defnyddiwr HTK> --ask-password http://htk.eng.cam.ac.uk/ftp/software/HTK-3.4.1.tar.gz`

`$ wget --user <eich enw defnyddiwr HTK> --ask-password http://htk.eng.cam.ac.uk/ftp/software/HTK-samples-3.4.1.tar.gz`

Bydd yn gofyn am eich cyfrinair yn y man.

Bydd ddwy ffeil, `HTK-3.4.1.tar.gz` a `HTK-samples-3.4.1.tar.gz` yn bodoli o fewn y cyfeiriadur 'voicebuilder'

## Cysylltu

Cysylltwch â techiaith@bangor.ac.uk os hoffwch chi creu a ddefnyddio testun-i-leferydd fwy parth benodol.
