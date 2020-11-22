plots.zip: %.png
	zip -j $@ *.png

%.png: extrapolate/*.py
	rm -f output.dat
	pytest -s tests/test_main.py

debug: extrapolate/*.py tests/*.py
	pytest -s tests/test_$@.py

clean:
	rm -f *.zip *.png output.dat

.PHONY: clean debug
