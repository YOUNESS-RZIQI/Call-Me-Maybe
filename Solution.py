# 1) Validate input files that are JSON format.


from typing import Union, Any
import json


def is_valide_json_file(file_name: str) -> Union[bool, Any]:
    """Validate a file is it a full JSON Format (True, False)"""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            result = json.load(file)
        return result
    except (json.JSONDecodeError, FileNotFoundError, PermissionError):
        return False
    except Exception as e:
        print(f"Error in (is_valide_json_file Function)\n{e}")
        return False


result = is_valide_json_file("data/input/function_calling_tests.json")

print(result)

# print(type(is_valide_json_file("tst.json")))
