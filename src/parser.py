from typing import List
import json
import traceback


class Parser:
    """ Parsing Tools. """
    @staticmethod
    def get_input_prompts_as_list() -> List:
        """ Convert Prompts file to List """
        try:
            with open("data/input/function_calling_tests.json", "r") as file:
                data = json.load(file)
                result = []
                for dict in data:
                    result.append(dict["prompt"])
                return result
        except Exception:
            print(traceback.print_exc(), "\n")
            return []

    @staticmethod
    def get_input_definitins_as_list() -> List:
        """ Convert Definitions file to List """
        try:
            with open("data/input/functions_definition.json", "r") as file:
                data = json.load(file)
                return data
        except Exception:
            print(traceback.print_exc())
            return []


print(len(Parser.get_input_definitins_as_list()[0]["parameters"]))
