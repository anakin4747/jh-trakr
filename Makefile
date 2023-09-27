new:
	python3 jh-trakr/main.py new

app:
	python3 jh-trakr/main.py applied

rej:
	python3 jh-trakr/main.py rejected

show:
	python3 jh-trakr/main.py show

show-working:
	python3 jh-trakr/main.py show working

show-applied:
	python3 jh-trakr/main.py show applied

show-rejected:
	python3 jh-trakr/main.py show rejected

freeze:
	pip3 freeze --all > requirements.txt

install: requirements.txt
	pip3 install -r requirements.txt

build: setup.py
	python3 setup.py build bdist_wheel

clean:
	rm -rf build dist jh_trakr.egg-info requirements.txt

super-clean:
	rm -rf build dist jh_trakr.egg-info requirements.txt \
		applied working job_apps.db

