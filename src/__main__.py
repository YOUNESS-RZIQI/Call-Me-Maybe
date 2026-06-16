from src.builder import PromptBuilder
from src.parser import Parser
import traceback
import sys
from typing import List
from src.models import DefinitionValidator
from src.decoding import constrain_decoding
import os


def pipline_process() -> None:
    """ Main Pipline Process """
    try:

        input_prompts: List[str] = Parser.get_input_prompts_as_list_of_strs()
        functions_def: List[
            DefinitionValidator] = Parser.get_input_definitions_objects()

        llm_prompts: List[str] = []
        for prompt in input_prompts:
            llm_prompts.append(
                PromptBuilder.build_final_prompt_string(prompt, functions_def))

        cd_outputs: List[str] = []
        for llm_prompt in llm_prompts:
            cd_outputs.append(constrain_decoding(llm_prompt))

        #check output is valid
        # write into data/outputs file.

    except Exception:
        sys.stderr.write("\033[91m")
        traceback.print_exc()
        sys.stdout.write("\033[0m")


if __name__ == "__main__":
    os.environ["HF_HOME"] = ".hf_cache"
    pipline_process()
