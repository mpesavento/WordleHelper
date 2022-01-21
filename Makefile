# Makefile for easy commands

update_deps:
	pip-compile requirements.in

run:
	python app.py
