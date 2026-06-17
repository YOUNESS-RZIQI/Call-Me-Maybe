import json
import sys
sys.path.append('.')
from llm_sdk import Small_LLM_Model

model = Small_LLM_Model()
vocab_path = model.get_path_to_vocab_file()
with open(vocab_path, "r", encoding="utf-8") as f:
    vocab = json.load(f)

# print 20 random items
import random
keys = list(vocab.keys())
for k in keys[1000:1020]:
    print(repr(k), vocab[k])
