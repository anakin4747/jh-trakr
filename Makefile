PROJ = jh_trakr
CLI = jh-trakr

build: setup.py uninstall
	python3 setup.py build bdist_wheel

install: build
	pip3 install dist/*.whl

uninstall:
	pip3 uninstall $(CLI)

test:
	pytest -v

clean:
	rm -rf build dist src/$(PROJ).egg-info
	find . -type d -name '__pycache__' -exec rm -r {} \;

super-clean: clean
	rm -rf applied working job_apps.db
