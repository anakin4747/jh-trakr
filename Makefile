


new:
	python3 jh-trakr/main.py new

app:
	python3 jh-trakr/main.py applied

rej:
	python3 jh-trakr/main.py rejected

build: setup.py
	python3 setup.py build bdist_wheel

clean:
	rm -rf build dist jh-trakr.egg-info
