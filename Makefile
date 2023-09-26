new:
	python3 jh-trakr/main.py new

app:
	python3 jh-trakr/main.py applied

rej:
	python3 jh-trakr/main.py rejected

freeze:
	pip3 freeze --all > requirements.txt

install: requirements.txt
	pip3 install -r requirements.txt

build: setup.py
	python3 setup.py build bdist_wheel

clean:
	rm -rf build dist jh_trakr.egg-info requirements.txt
