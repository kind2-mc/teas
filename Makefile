all: build

build:
	python setup.py sdist

run:
	python src $(args)