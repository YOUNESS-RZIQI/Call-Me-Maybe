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


def pipline_process() -> None:
    """ Main Pipline Process """
    try:

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

        print("End counting\n")

    except Exception:
        sys.stderr.write("\033[91m")
        traceback.print_exc()
        sys.stdout.write("\033[0m")


if __name__ == "__main__":
    pipline_process()


        # output_data = []
        # for i, s in enumerate(cd_strs):
        #     try:
        #         parsed = json.loads(s)

        #         # FIX 1: Restore original prompt verbatim (preserves double quotes
        #         # and other special chars that the LLM may have changed).
        #         parsed["prompt"] = input_prompts[i]

        #         # FIX 2: Convert parameters of type "number" to float.
        #         # The LLM generates whole numbers (e.g. 265) but the schema
        #         # expects floats (e.g. 265.0) for the "number" type.
        #         func_name = parsed.get("name")
        #         for func_def in functions_def_obj:
        #             if func_def.name == func_name:
        #                 for param_name, param_def in func_def.parameters.items():
        #                     if param_def.type in ("number", "decimal",
        #                                           "float", "num", "n"):
        #                         if param_name in parsed.get("parameters", {}):
        #                             parsed["parameters"][param_name] = float(
        #                                 parsed["parameters"][param_name])
        #                 break

        #         output_data.append(parsed)
        #     except json.JSONDecodeError as e:
        #         print("Error: ", e, " | Input: \n", s, "\n")