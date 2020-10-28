# Sgriptiau hyfforddi llais WISPR
# *Scripts for training the WISPR voice*

Mae'r ffolder hon yn cynnwys y sgriptiau ar gyfer hyfforddi llais MaryTTS gyda recordiadau a trawsgrifiadau [Corpws WISR](https://git.techiaith.bangor.ac.uk/Data-Porth-Technolegau-Iaith/Corpws-WISPR)

*This folder contains scripts for training a MaryTTS voice with recordings and transcripts from [Corpws WISR](https://git.techiaith.bangor.ac.uk/Data-Porth-Technolegau-Iaith/Corpws-WISPR)*

<br/>

Yn gyntaf, dylid estyn y data hyfforddi gyda'r sgript:

*First, you should fetch the training data with the script:*

`$ ./fetch-corpus.sh`

Ac yna defnyddiwch y sgript canlynol i hyfforddi..

*And then use the following script for training...*

`$ ./build.sh`


<br/>

Ar ôl i'r hyfforddi llais cwblhau, mae modd ei ychwanegu i MaryTTS gyda'r gorchymyn:

*After training has completed, you can install it into MaryTTS using the command:*

`$ voice-install-cy.sh wispr`
