# 1) Validate input files that are JSON format.


# from typing import
import json


def is_valide_json_file(file_name: str) -> bool:
    """Validate a file is it a full JSON Format (True, False)"""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            json.load(file)
        return True
    except (json.JSONDecodeError, FileNotFoundError, PermissionError):
        return False
    except Exception as e:
        print(f"Error in (is_valide_json_file Function)\n{e}")
        return False


print(is_valide_json_file("tssst.json"))
