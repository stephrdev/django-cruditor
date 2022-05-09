.PHONY: clean correct docs pytests tests coverage-html release
.ONESHELL: release

clean:
	rm -fr build/ dist/ htmlcov/ __pycache__
	poetry run make -C docs clean

correct:
	poetry run isort cruditor tests examples
	poetry run black -q cruditor tests examples

docs:
	poetry run make -C docs html

pytests:
	@PYTHONPATH=$(CURDIR):${PYTHONPATH} poetry run pytest

tests:
	@PYTHONPATH=$(CURDIR):${PYTHONPATH} poetry run pytest --cov --isort --flake8 --black

coverage-html: pytests
	poetry run coverage html

release:
	@VERSION=`poetry version -s`
	@echo About to release $${VERSION}
	@echo [ENTER] to continue; read
	git tag -a "$${VERSION}" -m "Version $${VERSION}" && git push --follow-tags
