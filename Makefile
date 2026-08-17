
PYTHON = python3
SCRIPT = a_maze_ing.py
VENV = venv
PIP = pip

.PHONY: install run debug clean lint build

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/$(PIP) install flake8 mypy

run:
	./$(VENV)/bin/$(PYTHON) $(SCRIPT) config.txt
debug:
	./$(VENV)/bin/$(PYTHON) -m pdb $(SCRIPT) config.txt
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/ dist/ *.egg-info/ *.tar
	rm -rf $(VENV)
lint:
	./$(VENV)/bin/flake8 . --exclude=$(VENV) 
	./$(VENV)/bin/mypy . --exclude=$(VENV) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

build:
	$(PYTHON) -m $(PIP) install build
	$(PYTHON) -m build
