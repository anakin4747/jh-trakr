PROJ = jh_trakr
CLI = jh

build: setup.py
	python3 setup.py build bdist_wheel

install: build requirements.txt
	pip3 install -r requirements.txt 
	pip3 install dist/*.whl

uninstall:
	pip3 uninstall $(CLI)

test:
	pytest --cov=$(PROJ) tests

clean:
	rm -rf build dist src/$(PROJ).egg-info
	find . -type d -name '__pycache__' -exec rm -r {} \;

super-clean: clean
	rm -rf applied working job_apps.db
