import re

class ValueMatcher:
    def is_valid_prefix(self, text: str) -> bool: raise NotImplementedError
    def match_full(self, text: str) -> int: raise NotImplementedError

class NumberMatcher(ValueMatcher):
    def is_valid_prefix(self, text: str) -> bool:
        return bool(re.match(r'^-?[0-9]*\.?[0-9]*$', text))
    def match_full(self, text: str) -> int:
        m = re.match(r'^-?[0-9]+(?:\.[0-9]+)?$', text)
        return len(text) if m else -1

class StringMatcher(ValueMatcher):
    def is_valid_prefix(self, text: str) -> bool:
        if not text: return True
        if text[0] != '"': return False
        quotes = text.count('"')
        if quotes > 2: return False
        if quotes == 2 and text[-1] != '"': return False
        return True
    def match_full(self, text: str) -> int:
        m = re.match(r'^"[^"]*"$', text)
        return len(text) if m else -1

class BooleanMatcher(ValueMatcher):
    def is_valid_prefix(self, text: str) -> bool:
        return "true".startswith(text) or "false".startswith(text)
    def match_full(self, text: str) -> int:
        if text == "true" or text == "false": return len(text)
        return -1

def check_template(text: str, parts: list, part_idx: int) -> bool:
    if not text:
        return True
    if part_idx >= len(parts):
        return False
        
    part = parts[part_idx]
    if isinstance(part, str):
        if text.startswith(part):
            return check_template(text[len(part):], parts, part_idx + 1)
        elif part.startswith(text):
            return True
        else:
            return False
    else:
        for i in range(1, len(text) + 1):
            val_str = text[:i]
            rem_str = text[i:]
            if part.match_full(val_str) == len(val_str):
                if check_template(rem_str, parts, part_idx + 1):
                    return True
        return part.is_valid_prefix(text)

parts = ['{\n"prompt": "What is 2+2?",\n"name": "fn_add",\n"parameters": {"a": ', NumberMatcher(), ', "b": ', NumberMatcher(), '}\n}']
tests = [
    '{\n"prompt": "W',
    '{\n"prompt": "What is 2+2?",\n"name": "fn_add",\n"parameters": {"a": 2',
    '{\n"prompt": "What is 2+2?",\n"name": "fn_add",\n"parameters": {"a": 2, "b": 2}',
    '{\n"prompt": "What is 2+2?",\n"name": "fn_add",\n"parameters": {"a": 2, "b": 2}\n',
    '{\n"prompt": "What is 2+2?",\n"name": "fn_add",\n"parameters": {"a": 2, "b": 2}\n}',
    '{\n"prompt": "What is 2+2?",\n"name": "fn_add",\n"parameters": {"a": 2, "b": 2}\n} EXTRA',
    '{\n"prompt": "What is 2+2?",\n"name": "fn_add",\n"parameters": {"a": 2.5',
    '{\n"prompt": "What is 2+2?",\n"name": "fn_add",\n"parameters": {"a": -2.5, "b": 3',
]

for t in tests:
    print(f"Match {repr(t)}: {check_template(t, parts, 0)}")

