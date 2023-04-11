help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  install       to create poetry environment"
	@echo "  start       to start bot"

install:
	pip install poetry && \
	poetry install

start:
	poetry run python __main__.py