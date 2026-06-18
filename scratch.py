from llm_sdk import Small_LLM_Model
import json

model = Small_LLM_Model()
print(repr(model.decode([16]))) # 16 is space? or something? let's find ' 3'
tokens = model.encode(" 3").tolist()[0]
print(tokens)
print(repr(model.decode(tokens)))
print(repr(model.decode([tokens[0]])))

tokens = model.encode("3").tolist()[0]
print(tokens)
print(repr(model.decode([tokens[0]])))
