UV = uv
PYTHON = python

UV_CACHE_DIR ?= .cache/uv
HF_HOME ?= .cache/huggingface

# if you'd like to use a different data. uncomment the ARGS below, and also the one in run & debug.
# and you can change data path to wherever you want.
# ARGS = --functions_definition /home/yrziqi/goinfre/Call-Me-Maybe/data2/input/functions_definition.json \
#   --input /home/yrziqi/goinfre/Call-Me-Maybe/data2/input/function_calling_tests.json \
#   --output /home/yrziqi/goinfre/Call-Me-Maybe/data2/output/function_calls.json

install:

	pip install flake8 mypy pydantic uv

run:
	UV_CACHE_DIR=$(UV_CACHE_DIR) HF_HOME=$(HF_HOME) $(UV) run $(PYTHON) -m src
# 	UV_CACHE_DIR=$(UV_CACHE_DIR) HF_HOME=$(HF_HOME) $(UV) run $(PYTHON) -m src $(ARGS)

debug:
	UV_CACHE_DIR=$(UV_CACHE_DIR) HF_HOME=$(HF_HOME) gdb $(UV) run $(PYTHON) -m src
# 	UV_CACHE_DIR=$(UV_CACHE_DIR) HF_HOME=$(HF_HOME) gdb --args $(UV) run $(PYTHON) -m src $(ARGS)

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .mypy_cache
	rm -f *.pyc */*.pyc */*/*.pyc

lint:
	python3 -m flake8 * || true
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs || true


.PHONY: install run debug clean lint