PYTHON = python3
POETRY = poetry
MAIN = pac-man.py
CONFIG = config.json
OUTPUT = highscores.json

all: run

install:
	pip install poetry
	$(POETRY) install --with dev

run:
	$(POETRY) run $(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(POETRY) run $(PYTHON) -m pdb $(MAIN) $(CONFIG)

build:
	pip install pyinstaller
	$(POETRY) run pyinstaller --name "Pac-Man42" \
	--add-data "assets:assets" \
	--add-data "config.json:." \
	--add-data "configuration_files:configuration_files" \
	--hidden-import "pygame.mixer" \
	--hidden-import "pygame.font" \
	--windowed \
	--noconfirm \
	$(MAIN)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache .ruff_cache
	rm -rf packaging/build dist build *.spec
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores \
	       --ignore-missing-imports --disallow-untyped-defs \
	       --check-untyped-defs

.PHONY: install run debug build clean lint