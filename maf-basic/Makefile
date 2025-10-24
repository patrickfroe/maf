PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: install run test

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) -m maf_basic.cli

test:
	$(PYTHON) -m pytest
