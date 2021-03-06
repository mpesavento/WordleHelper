# Makefile for easy commands

new_env:
	python3 -m venv ./venv && \
	pip install requirements.txt

update_deps:
	pip-compile requirements.in

run:
	python app.py

run_dev:
	FLASK_APP=app FLASK_ENV=development flask run

run_cli:
	python wordle_helper/wordle_filters.py