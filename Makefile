.PHONY: install run debug clean lint lint-strict

UV = uv
PYTHON = python

UV_CACHE_DIR ?= .cache/uv
HF_HOME ?= .cache/huggingface

install:

	pip install flake8 mypy pydantic uv

run:
	UV_CACHE_DIR=$(UV_CACHE_DIR) HF_HOME=$(HF_HOME) $(UV) run $(PYTHON) -m src $(ARGS)

debug:
	UV_CACHE_DIR=$(UV_CACHE_DIR) HF_HOME=$(HF_HOME) gdb --args $(UV) run $(PYTHON) -m src $(ARGS)

clean:
	rm -rf __pycache__ .mypy_cache

lint:
	$(UV) run flake8 . && $(UV) run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(UV) run flake8 . && $(UV) run mypy . --strict --ignore-missing-imports

