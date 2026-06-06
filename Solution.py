# 1) Validate input files that are JSON format.


# from typing import
import json


def is_valide_json_file(file_name: str) -> bool:
    """Is the format of the file is JSON"""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            json.load(file)
        return True
    except json.JSONDecodeError:
        return False


print(is_valide_json_file("tst.json"))
