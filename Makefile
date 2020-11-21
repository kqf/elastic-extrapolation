plots.zip: %.png
	zip -j $@ *.png

%.png: extrapolate/*.py
	rm -f output.dat
	pytest -s tests/test_main.py

debug: extrapolate/*.py tests/*.py
	python pytest/test_$@.py
