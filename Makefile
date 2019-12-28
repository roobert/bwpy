APP=bwpy

install:
	@poetry install

clean:
	@rm -vrf ${APP}.egg-info venv

dev-run:
	@poetry run ${APP}

setup-convert:
	@dephell deps convert

# venv can be useful for debugging..
venv:
	@virtualenv venv
	@echo "# run:"
	@echo "source venv/bin/activate"