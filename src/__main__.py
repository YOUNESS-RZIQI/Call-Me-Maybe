from src.builder import PromptBuilder
from src.parser import Parser
import traceback
import sys
from typing import List, Dict
from src.models import DefinitionValidator
from src.decoding import constrain_decoding


def pipline_process() -> None:
    """ Main Pipline Process """
    try:

        input_prompts: List[str] = Parser.get_input_prompts_as_list_of_strs()
        functions_def_obj: List[
            DefinitionValidator] = Parser.get_input_definitions_objects()

        functions_def_list: List[str] = []
        for obj in functions_def_obj:
            functions_def_list.append(obj.name)

        final_llm_prompts: List[str] = []
        for prompt in input_prompts:
            final_llm_prompts.append(
                PromptBuilder.build_final_prompt_string(prompt, functions_def_obj))

        cd_strs: List[str] = []
        input_prompt_index: int = 0

        for llm_prompt in final_llm_prompts:
            cd_strs.append(constrain_decoding(llm_prompt,
                            input_prompts[input_prompt_index],
                            functions_def_list))
            input_prompt_index += 1

        #check output is valid
        # write into data/outputs file.

    except Exception:
        sys.stderr.write("\033[91m")
        traceback.print_exc()
        sys.stdout.write("\033[0m")


if __name__ == "__main__":
    pipline_process()
