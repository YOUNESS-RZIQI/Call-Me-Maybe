from typing import List
import json
import traceback
from src.models import PromptValidator, DefinitionValidator


class Parser:
    """ Parsing Tools. """
    @staticmethod
    def get_input_prompts_as_list_of_strs(path: str = "data/input/function_calling_tests.json") -> List[str]:
        """ Convert Prompts file to List Strings """
        try:
            with open(path, "r") as file:
                data = json.load(file)
                prompts_list = []
                for item in data:
                    validated_prompt = PromptValidator(**item) 
                    prompts_list.append(validated_prompt.prompt)
                return prompts_list
        except Exception:
            print(traceback.print_exc(), "\n")
            return []

    @staticmethod
    def get_input_definitions_objects(path: str = "data/input/functions_definition.json") -> List[DefinitionValidator]:
        """ Convert Definitions file to Definitions Objects List """
        try:
            with open(path, "r") as file:
                data = json.load(file)
                definitions_list = []
                for item in data:
                    validated_deffinition = DefinitionValidator(**item)
                    definitions_list.append(validated_deffinition)
                return definitions_list
        except Exception:
            print(traceback.print_exc())
            return []


