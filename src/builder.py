from src.models import DefinitionValidator
from typing import List


class PromptBuilder:
    """ Builder Tools """
    @staticmethod
    def build_final_prompt_string(prompts: str, definitions_list: List[DefinitionValidator]) -> str:
        """ Build Final Prompt String """
        final_string = ""
        i = 1
        for function in definitions_list:
            final_string += f"Function {i}: {function.name}({', '.join([f'{key}: {value.type}' for key, value in function.parameters.items()])})"
            i += 1
        final_string += f' Request: ({prompts}), ' + \
            'expected JSON schema: {\n"prompt": "...",\n"name": "...",\n"parameters": {"argment1": value1, ...}\n}, JSON: '
        return final_string
