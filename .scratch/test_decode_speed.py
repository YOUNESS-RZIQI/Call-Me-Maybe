import os
os.environ["HF_HOME"] = "/goinfre/yrziqi/Call-Me-Maybe/.hf_cache"
import time
import json
import sys
sys.path.append('.')
from llm_sdk import Small_LLM_Model

model = Small_LLM_Model()
vocab_path = model.get_path_to_vocab_file()
with open(vocab_path, "r", encoding="utf-8") as f:
    vocab = json.load(f)

start = time.time()
id_to_str = {}
count = 0
for t, i in vocab.items():
    id_to_str[i] = model.decode([i])
    count += 1
    if count == 5000:
        break
end = time.time()
print(f"5000 tokens decoded in {end - start:.2f} seconds")
