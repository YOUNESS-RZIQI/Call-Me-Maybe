# import json
# from typing import List, Dict, Optional
# from src.models import DefinitionValidator
# from llm_sdk.llm_sdk import Small_LLM_Model

# class PrefixParser:
#     def __init__(self, text: str):
#         self.text = text
#         self.pos = 0
#         self.length = len(text)

#     def eof(self) -> bool:
#         return self.pos >= self.length

#     def skip_ws(self) -> None:
#         while not self.eof() and self.text[self.pos] in ' \t\n\r':
#             self.pos += 1

#     def match(self, target: str) -> bool:
#         self.skip_ws()
#         if self.eof():
#             return False
        
#         if target.startswith(self.text[self.pos:]):
#             self.pos = self.length
#             return False
            
#         if self.text.startswith(target, self.pos):
#             self.pos += len(target)
#             return True
            
#         raise ValueError(f"Expected '{target}'")

#     def match_string_prefix(self, allowed_strings: Optional[List[str]] = None) -> Optional[str]:
#         self.skip_ws()
#         if self.eof(): return None
#         if self.text[self.pos] != '"':
#             raise ValueError("Expected string")
        
#         end = self.pos + 1
#         escaped = False
#         while end < self.length:
#             if escaped:
#                 escaped = False
#             elif self.text[end] == '\\':
#                 escaped = True
#             elif self.text[end] == '"':
#                 break
#             end += 1
            
#         if end == self.length:
#             if allowed_strings is not None:
#                 partial = self.text[self.pos+1:]
#                 if not any(s.startswith(partial) for s in allowed_strings):
#                     raise ValueError(f"String prefix '{partial}' does not match allowed")
#             self.pos = self.length
#             return None
            
#         val = json.loads(self.text[self.pos:end+1])
#         if allowed_strings is not None and val not in allowed_strings:
#             raise ValueError(f"String '{val}' not allowed")
            
#         self.pos = end + 1
#         return val

#     def match_number(self) -> bool:
#         self.skip_ws()
#         if self.eof(): return False
        
#         start = self.pos
#         valid_chars = set("-+0123456789.eE")
#         while self.pos < self.length and self.text[self.pos] in valid_chars:
#             self.pos += 1
            
#         if self.pos == self.length:
#             s = self.text[start:]
#             if s == "-": return False
#             return False
            
#         try:
#             float(self.text[start:self.pos])
#             return True
#         except ValueError:
#             raise ValueError("Invalid number")

#     def match_boolean(self) -> bool:
#         self.skip_ws()
#         if self.eof(): return False
        
#         if "true".startswith(self.text[self.pos:]):
#             self.pos = self.length
#             return False
#         if "false".startswith(self.text[self.pos:]):
#             self.pos = self.length
#             return False
            
#         if self.text.startswith("true", self.pos):
#             self.pos += 4
#             return True
#         if self.text.startswith("false", self.pos):
#             self.pos += 5
#             return True
            
#         raise ValueError("Invalid boolean")


# class JSONPrefixValidator:
#     def __init__(self, definitions: List[DefinitionValidator]) -> None:
#         self.definitions = definitions

#     def is_valid_prefix(self, text: str) -> bool:
#         try:
#             p = PrefixParser(text)
#             if not p.match("{"): return True
#             if not p.match_string_prefix(["name"]): return True
#             if not p.match(":"): return True
            
#             func_names = [d.name for d in self.definitions]
#             name = p.match_string_prefix(func_names)
#             if name is None: return True
            
#             if not p.match(","): return True
#             if not p.match_string_prefix(["parameters"]): return True
#             if not p.match(":"): return True
#             if not p.match("{"): return True
            
#             func_def = next(d for d in self.definitions if d.name == name)
#             params = func_def.parameters
            
#             parsed_keys = set()
            
#             while True:
#                 p.skip_ws()
#                 if p.eof(): return True
#                 if p.text.startswith("}", p.pos):
#                     p.pos += 1
#                     break
                    
#                 if parsed_keys:
#                     if not p.match(","): return True
                    
#                 key = p.match_string_prefix(list(params.keys()))
#                 if key is None: return True
#                 if key in parsed_keys:
#                     raise ValueError("Duplicate key")
#                 parsed_keys.add(key)
                
#                 if not p.match(":"): return True
                
#                 expected_type = params[key].type
#                 if expected_type in ("string", "str"):
#                     if p.match_string_prefix() is None: return True
#                 elif expected_type in ("number", "int", "float"):
#                     if not p.match_number(): return True
#                 elif expected_type == "boolean":
#                     if not p.match_boolean(): return True
#                 else:
#                     pass # Fallback for unsupported types
                    
#             if not p.match("}"): return True
            
#             p.skip_ws()
#             if not p.eof():
#                 raise ValueError("Extra data after JSON")
                
#             return True
#         except ValueError:
#             return False

# class ConstrainedDecoder:
#     def __init__(self, llm: Small_LLM_Model, definitions: List[DefinitionValidator]) -> None:
#         self.llm = llm
#         self.validator = JSONPrefixValidator(definitions)
#         self.token_to_string = self._load_vocabulary()

#     def _load_vocabulary(self) -> Dict[int, str]:
#         vocab_path = self.llm.get_path_to_vocab_file()
#         with open(vocab_path, 'r', encoding='utf-8') as f:
#             vocab = json.load(f)
#             # HF vocabs usually map string to int
#             return {v: k for k, v in vocab.items()}

#     def decode(self, prompt: str, max_tokens: int = 256) -> str:
#         input_ids = self.llm.encode(prompt).tolist()[0]
#         base_len = len(self.llm.decode(input_ids))
#         decoded_string = ""
        
#         for _ in range(max_tokens):
#             logits = self.llm.get_logits_from_input_ids(input_ids)
            
#             sorted_token_ids = sorted(range(len(logits)), key=lambda i: logits[i], reverse=True)
            
#             valid_token_found = False
#             for token_id in sorted_token_ids:
#                 test_ids = input_ids + [token_id]
#                 test_string = self.llm.decode(test_ids)
                
#                 generated_part = test_string[base_len:]
                
#                 if self.validator.is_valid_prefix(generated_part):
#                     input_ids.append(token_id)
#                     decoded_string = generated_part
#                     valid_token_found = True
#                     break
                    
#             if not valid_token_found:
#                 # If no valid token, just stop
#                 break
                
#             # Stop condition: generated part is a complete valid JSON object
#             # Our validator ensures it's strict. If it ends with "}" and is valid, and curly braces match
#             if decoded_string.strip().endswith("}") and decoded_string.count("{") == decoded_string.count("}"):
#                 # Need to be careful because parameters might have no closing brace if empty
#                 if self.validator.is_valid_prefix(decoded_string):
#                     try:
#                         json.loads(decoded_string)
#                         break
#                     except json.JSONDecodeError:
#                         pass
                        
#         return decoded_string


