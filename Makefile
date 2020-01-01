APP=bwpy
VERSION := $(shell python -c 'import toml; print(toml.load("pyproject.toml")["tool"]["poetry"]["version"])')

install:
	@poetry install

clean:
	@rm -vrf ${APP}.egg-info venv

publish:
	$(shell echo "version = \"${VERSION}\"" > bwpy/version.py)
	@poetry build
	@poetry publish

dev-run:
	@poetry run ${APP}

setup-convert:
	@dephell deps convert

# venv can be useful for debugging..
venv:
	@virtualenv venv
	@echo "# run:"
	@echo "source venv/bin/activate"
