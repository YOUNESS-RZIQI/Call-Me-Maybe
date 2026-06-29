from src.builder import PromptBuilder
from src.parser import Parser
import traceback
import sys
from typing import List
from src.models import DefinitionValidator
from src.decoding import function_calling
import json
import time
import os


def pipline_process(
        inpt_prompt_path: str = "data/input/function_calling_tests.json",
        functions_def_path: str = "data/input/functions_definition.json",
        output_path: str = "data/output/function_calls.json") -> None:

    """ Main Pipline Process """
    try:

        input_prompts: List[str] = \
            Parser.get_input_prompts_as_list_of_strs(inpt_prompt_path)
        functions_def_obj: List[DefinitionValidator] = \
            Parser.get_input_definitions_objects(functions_def_path)

        final_llm_prompts: List[str] = []
        for prompt in input_prompts:
            final_llm_prompts.append(
                PromptBuilder.build_final_prompt_string(prompt,
                                                        functions_def_obj))

        cd_results: List[dict] = []

        from llm_sdk import Small_LLM_Model
        model: Small_LLM_Model = Small_LLM_Model()

        start_time: float = time.time()
        print("start counting\n")

        for input_prompt_index, llm_prompt in enumerate(final_llm_prompts):
            cd_results.append(function_calling(
                model, llm_prompt, input_prompts[input_prompt_index],
                functions_def_path))

        output_dir: str = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cd_results, f, indent=4)

        end_time: float = time.time()
        print(f"End counting in {(end_time - start_time) / 60} minutes\n")

    except Exception:
        sys.stderr.write("\033[91m")
        traceback.print_exc()
        sys.stdout.write("\033[0m")
        print("\n\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--functions_definition",
        default="./data/input/functions_definition.json"
    )

    parser.add_argument(
        "--input",
        default="./data/input/function_calling_tests.json"
    )

    parser.add_argument(
        "--output",
        default="./data/output/function_calls.json"
    )

    args = parser.parse_args()

    pipline_process(
        inpt_prompt_path=args.input,
        functions_def_path=args.functions_definition,
        output_path=args.output,
    )
