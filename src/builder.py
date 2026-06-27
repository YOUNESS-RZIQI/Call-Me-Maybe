from src.models import DefinitionValidator
from typing import List


class PromptBuilder:
    """ Builder Tools """
    @staticmethod
    def build_final_prompt_string(
        prompt: str, definitions_list: List[DefinitionValidator]
    ) -> str:
        """ Build Final Prompt String """
        final_string = ""
        i = 0
        for function in definitions_list:
            params = ', '.join(
                f'{key}: {value.type}'
                for key, value in function.parameters.items()
            )
            final_string += (
                f"Function {i}: {function.name}"
                f"({params}), "
                f"Descreption: {function.description}\n"
            )
            i += 1
        final_string += (
            f' Request: ({prompt}), '
            + 'Result is Function Number: '
        )
        return final_string
