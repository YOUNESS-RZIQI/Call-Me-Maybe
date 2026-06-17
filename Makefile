UV_CACHE_DIR:=.cache/uv
HF_HOME:=.cache/huggingface

run:
	export UV_CACHE_DIR=$(UV_CACHE_DIR) && export HF_HOME=$(HF_HOME) && uv run python3 -m src


install:
	uv sync --cache-dir=$(UV_CACHE_DIR)
