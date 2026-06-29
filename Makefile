UV = uv
PYTHON = python

UV_CACHE_DIR = .cache/uv
HF_HOME = .cache/huggingface

# Uncomment to use custom input/output paths.
# ARGS = --functions_definition /path/to/functions_definition.json \
#        --input /path/to/function_calling_tests.json \
#        --output /path/to/function_calls.json

.PHONY: install run debug clean lint

install:
	pip install uv flake8 mypy
	UV_CACHE_DIR=$(UV_CACHE_DIR) HF_HOME=$(HF_HOME) $(UV) sync

run:
	UV_CACHE_DIR=$(UV_CACHE_DIR) HF_HOME=$(HF_HOME) \
	$(UV) run $(PYTHON) -m src
#	UV_CACHE_DIR=$(UV_CACHE_DIR) HF_HOME=$(HF_HOME) \
#	$(UV) run $(PYTHON) -m src $(ARGS)

debug:
	UV_CACHE_DIR=$(UV_CACHE_DIR) HF_HOME=$(HF_HOME) \
	gdb --args $(UV) run $(PYTHON) -m src
#	UV_CACHE_DIR=$(UV_CACHE_DIR) HF_HOME=$(HF_HOME) \
#	gdb --args $(UV) run $(PYTHON) -m src $(ARGS)

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache

lint:
	$(UV) run flake8 . || true
	$(UV) run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs || true