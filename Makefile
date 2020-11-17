PYTHON_VERSION      := $(shell cut -d '/' -f 1 .python-version)
PYTHON_BIN          := python$(shell cut -d '.' -f 1-2 .python-version)
VIRTUALENV_NAME     := $(shell cut -d '/' -f 3 .python-version)

default:
	@pytest -s

devinstall:
	pyenv install --skip-existing ${PYTHON_VERSION}
	pyenv virtualenv --force --python=${PYTHON_BIN} ${PYTHON_VERSION} ${VIRTUALENV_NAME}
	pip install --editable .[dev,test]
