plots.zip: %.png
	zip -j $@ *.png

%.png: extrapolate/*.py
	rm -f output.dat
	python extrapolate/main.py
