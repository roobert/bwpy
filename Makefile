APP=bwpy
VERSION := $(shell python -c 'import toml; print(toml.load("pyproject.toml")["tool"]["poetry"]["version"])')

install:
	@poetry install

clean:
	@rm -vrf ${APP}.egg-info venv

dev-run:
	@poetry run ${APP}

setup-convert:
	@dephell deps convert

venv:
	@virtualenv venv
	@echo "# run:"
	@echo "source venv/bin/activate"

version-bump-patch:
	@poetry version patch
	$(shell echo "version = \"${VERSION}\"" > ${APP}/version.py)

version-bump-minor:
	@poetry version minor
	$(shell echo "version = \"${VERSION}\"" > ${APP}/version.py)

version-bump-major:
	@poetry version major
	$(shell echo "version = \"${VERSION}\"" > ${APP}/version.py)

version-update:
	$(shell echo "version = \"${VERSION}\"" > ${APP}/version.py)

publish: setup-convert version-update
	@poetry build
	@poetry publish

