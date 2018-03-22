default: build

build: 
	docker build -t techiaith/marytts .

run:
	docker run --name marytts -p 59125:59125 -it \
		-v ${PWD}/voice-builder:/home/marytts/voice-builder \
		-v ${PWD}/texts:/home/marytts/texts \
		techiaith/marytts bash

stop:
	docker stop marytts
	docker rm marytts

clean:
	docker rmi techiaith/marytts

github:
	 git clone https://github.com/techiaith/marytts.git
	 cd marytts && git checkout branch marytts-lang-cy
	 
