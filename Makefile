all: build

build:
	python setup.py sdist

run:
	python src $(args)

test:
	./scripts/tests.sh

clean:
	rm -rf dist
	rm -f src/tests/*.pyc src/*.pyc MANIFEST

.PHONY: build run test clean