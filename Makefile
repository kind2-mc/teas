all: build

build:
	python setup.py sdist

run:
	python src $(args)

test:
	nosetests-2.7 -v src/tests/*.py

clean:
	rm -rf dist src/tests/*.pyc
	rm MANIFEST