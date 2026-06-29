from typing import List
import json
from src.models import PromptValidator, DefinitionValidator
import traceback
import sys


class Parser:
    """Utility methods for parsing project input files."""
    @staticmethod
    def get_input_prompts_as_list_of_strs(path: str) -> List[str]:
        """Parse the prompts JSON file into a list of prompt strings."""
        try:
            with open(path, "r") as file:
                data: List[dict] = json.load(file)
                prompts_list: List[str] = []
                for item in data:
                    validated_prompt: PromptValidator = PromptValidator(**item)
                    prompts_list.append(validated_prompt.prompt)
                return prompts_list
        except Exception:
            sys.stderr.write("\033[91m")
            traceback.print_exc()
            print("\n\n")
            sys.stdout.write("\033[0m")
            return []

    @staticmethod
    def get_input_definitions_objects(path: str) -> List[DefinitionValidator]:
        """Parse the function definitions JSON file into validated objects."""
        try:
            with open(path, "r") as file:
                data: List[dict] = json.load(file)
                definitions_list: List[DefinitionValidator] = []
                for item in data:
                    validated_definition: DefinitionValidator = \
                        DefinitionValidator(**item)
                    definitions_list.append(validated_definition)
                return definitions_list
        except Exception:
            sys.stderr.write("\033[91m")
            traceback.print_exc()
            print("\n\n")
            sys.stdout.write("\033[0m")
            return []
