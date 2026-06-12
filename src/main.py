from builder import PromptBuilder
from parser import Parser
import traceback
import sys
from typing import List
from models import DefinitionValidator


def pipeline_process() -> None:
    """ Main Pipline Process """
    try:
        input_prompts: List[str] = Parser.get_input_prompts_as_list_of_strs()
        functions_def: List[DefinitionValidator] = Parser.get_input_definitions_objects()

        llm_prompts: List[str] = []
        for prompt in input_prompts:
            llm_prompts.append(PromptBuilder.build_final_prompt_string(prompt, functions_def))

        print(llm_prompts)
    except Exception:
        sys.stderr.write("\033[91m")
        traceback.print_exc()
        sys.stdout.write("\033[0m")
        print("\nhi\n")


pipeline_process()