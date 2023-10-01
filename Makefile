PROJ = src/jh_trakr

new:
	python3 $(PROJ)/main.py new

app:
	python3 $(PROJ)/main.py applied

rej:
	python3 $(PROJ)/main.py rejected

show:
	python3 $(PROJ)/main.py show

show-working:
	python3 $(PROJ)/main.py show working

show-applied:
	python3 $(PROJ)/main.py show applied

show-rejected:
	python3 $(PROJ)/main.py show rejected

test:
	pytest -v

build: setup.py test
	python3 setup.py build bdist_wheel

clean:
	rm -rf build dist $(PROJ)/$(PROJ).egg-info requirements.txt \
		__pycache__ $(PROJ)/__pycache__ tests/__pycache__


super-clean:
	rm -rf build dist $(PROJ).egg-info requirements.txt \
		__pycache__ $(PROJ)/__pycache__ tests/__pycache__ \
		applied working job_apps.db
