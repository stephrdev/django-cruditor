.PHONY: clean tests cov docs runserver release

VERSION = $(shell python -c "print(__import__('cruditor').__version__)")

clean:
	rm -fr docs/_build build/ dist/
	pipenv run make -C docs clean

tests:
	pipenv run py.test --cov

cov: tests
	pipenv run coverage html
	@echo open htmlcov/index.html

docs:
	pipenv run make -C docs linkcheck html
	@echo open docs/_build/html/index.html

runserver:
	pipenv run examples/manage.py runserver

release:
	@echo About to release ${VERSION}; read
	pipenv run python setup.py sdist upload
	python setup.py bdist_wheel upload
	git tag -a "${VERSION}" -m "Version ${VERSION}" && git push --follow-tags

