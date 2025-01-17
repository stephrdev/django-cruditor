.PHONY: clean correct docs pytests tests coverage-html release
.ONESHELL: release

clean:
	rm -fr build/ dist/ htmlcov/ __pycache__
	uv run make -C docs clean

correct:
	uv run ruff check --fix --select I
	uv run ruff format

docs:
	uv run make -C docs html

lint:
	uv run ruff check
	uv run ruff format --check --diff

pytests:
	uv run pytest $(ARGS)

tests: lint pytests

coverage-html:
	uv run pytest --cov --cov-report=html ${ARGS}

release:
	@VERSION=`grep -E "^version =" pyproject.toml | cut -d\" -f2`
	@echo About to release $${VERSION}
	@echo [ENTER] to continue; read
	git tag -a "$${VERSION}" -m "Version $${VERSION}" && git push --follow-tags
