from builder import PromptBuilder
from parser import Parser
import traceback
import sys
from typing import List, Any
from models import DefinitionValidator
from llm_sdk import Small_LLM_Model
import numpy as np


def pipline_process() -> None:
    """ Main Pipline Process """
    try:

        input_prompts: List[str] = Parser.get_input_prompts_as_list_of_strs()
        functions_def: List[DefinitionValidator] = Parser.get_input_definitions_objects()

        llm_prompts: List[str] = []
        for prompt in input_prompts:
            llm_prompts.append(PromptBuilder.build_final_prompt_string(prompt, functions_def))

        module: Small_LLM_Model = Small_LLM_Model()
        for llm_prompt in llm_prompts:
            result: str = llm_prompt
            ids: List[int] = module.encode(result)
            for _ in range(50):
                logits: Any = module.get_logits_from_input_ids(ids)
                next_token_in: int = int(np.argmax(logits[0].tolist())) # is the logits are tensor.
                ids.append(next_token_in)
            result = module.decode(ids)
            print(result, "\n")

    except Exception:
        sys.stderr.write("\033[91m")
        traceback.print_exc()
        sys.stdout.write("\033[0m")
        print("\nhi\n")


if __name__ == "__main__":
    pipline_process()
