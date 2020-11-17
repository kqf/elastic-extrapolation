plots.zip: %.png
	zip -j $@ *.png

%.png: extrapolate/*.py
	python extrapolate/main.py
