import os
os.environ["HF_HOME"] = "/goinfre/yrziqi/Call-Me-Maybe/.hf_cache"
import sys
sys.path.append('.')
from llm_sdk import Small_LLM_Model

model = Small_LLM_Model()
print("Model loaded successfully!")
