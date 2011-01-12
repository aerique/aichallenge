all: playback/movie.gif


playback/frame00001.png: *.py *.png
	python engine.py

game: playback/frame00001.png


playback/movie.gif: playback/frame00001.png
	convert -loop 0 playback/frame*.png playback/movie.gif
	ln -s playback/movie.gif movie.gif

movie: playback/movie.gif


clean:
	-rm -Rf playback/*.png
	-rm -Rf playback/movie.gif
	-rm -Rf movie.gif


.PHONY: all clean movie game