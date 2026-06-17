import sys
sys.path.append('.')
from llm_sdk import Small_LLM_Model
import json

model = Small_LLM_Model()
vocab_path = model.get_path_to_vocab_file()
print(f"Vocab path: {vocab_path}")

with open(vocab_path, 'r') as f:
    vocab = json.load(f)

print(f"Vocab size: {len(vocab)}")
# Show some interesting tokens
samples = ['{', '{\n', '"prompt"', ':', ' "']
for s in samples:
    encoded = model.encode(s)[0].tolist()
    print(f"Encode '{s}': {encoded}")
    for tk in encoded:
        print(f"  {tk} -> {model.decode([tk])}")

