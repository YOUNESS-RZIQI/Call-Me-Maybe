from src.builder import PromptBuilder
from src.parser import Parser
import traceback
import sys
from typing import List
from src.models import DefinitionValidator
from src.decoding import constrain_decoding
import json
import os
from llm_sdk import Small_LLM_Model
import time


def pipline_process() -> None:
    """ Main Pipline Process """
    try:
        start_time = time.time()
        model: Small_LLM_Model = Small_LLM_Model()
        print("start counting\n")

        input_prompts: List[str] = Parser.get_input_prompts_as_list_of_strs()
        functions_def_obj: List[
            DefinitionValidator] = Parser.get_input_definitions_objects()

        final_llm_prompts: List[str] = []
        for prompt in input_prompts:
            final_llm_prompts.append(
                PromptBuilder.build_final_prompt_string(prompt,
                                                        functions_def_obj))

        cd_results: List[dict] = []

        for input_prompt_index, llm_prompt in enumerate(final_llm_prompts):
            cd_results.append(constrain_decoding(
                model, llm_prompt, input_prompts[input_prompt_index]))

        os.makedirs("data/output", exist_ok=True)
        with open("data/output/function_calls.json", "w") as f:
            json.dump(cd_results, f, indent=4)

        end_time = time.time()
        print(f"End counting in {(end_time - start_time) / 60} minutes\n")

    except Exception:
        sys.stderr.write("\033[91m")
        traceback.print_exc()
        sys.stdout.write("\033[0m")


if __name__ == "__main__":
    pipline_process()
