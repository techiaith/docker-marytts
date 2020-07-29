default: build


build: 
	if [ ! -d "marytts" ]; then \
            git clone https://github.com/techiaith/marytts.git; \
        fi 
	docker build --rm -t techiaith/marytts .

run:
	docker run --name marytts --restart=always \
    	-it  \
	-v ${PWD}/voices/:/voices \
	techiaith/marytts bash

stop:
	docker stop marytts
	docker rm marytts

clean:
	docker rmi techiaith/marytts

