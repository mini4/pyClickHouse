PYTHON ?= python3

VENV_DIR = .env/
VENV_BIN = ${VENV_DIR}bin/

TEST_ARGS ?= -x --pdb


clean:
	@rm -rf ${VENV_DIR} *.egg-info/ .pytest_cache/

install: clean
	@${PYTHON} -mvenv ${VENV_DIR}
	@${VENV_BIN}pip install -e .[dev]

test:
	@${VENV_BIN}coverage run -m pytest tests
	@${VENV_BIN}coverage report -m

ptw:
	@${VENV_BIN}ptw --runner "${VENV_BIN}pytest -vv --testmon ${TEST_ARGS}"

lint:
	@${VENV_BIN}isort --check-only --diff clickhouse tests
	@${VENV_BIN}flake8 --max-line-length=99 clickhouse tests

blackify:
	@${VENV_BIN}black -S --line-length=99 clickhouse tests
	@${VENV_BIN}isort clickhouse tests

cli:
	@${VENV_BIN}python
