PROJECT_PATH=venv/
PYTHON=$(PROJECT_PATH)bin/python
PIP=$(PROJECT_PATH)bin/pip

black-all:
	black . --config black.toml

build:
	mkdir _media
	pip install -r requirements.txt
	$(PYTHON) init_db.py

run:
	$(PYTHON) bot.py
