# Validate input files that are JSON format.

# from typing import

import json


def is_valide_json_file(file_name: str):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            json.load(file)
        return True
    except json.JSONDecodeError:
        return False
