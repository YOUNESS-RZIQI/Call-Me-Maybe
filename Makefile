UV_CACHE_DIR:=.cache/uv
HF_HOME:=.cache/huggingface

install:
	uv sync --cache-dir=$(UV_CACHE_DIR)
