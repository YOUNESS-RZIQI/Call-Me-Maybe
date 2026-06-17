from enum import Enum, auto
from llm_sdk import Small_LLM_Model
import numpy as np
from typing import List, Dict
import sys
import traceback
from src.models import DefinitionValidator


class States(Enum):
    """States for constrained decoding"""
    FUNCTION_NAME = auto()
    PARAMETERS = auto()


def constrain_decoding(llm_prompt: str, input_prompt: str) -> str:
    """ Constrained Decoding for JSON """
    try:
        input_prompts: List[str] = Parser.get_input_prompts_as_list_of_strs()
        functions_def: List[
            DefinitionValidator] = Parser.get_input_definitions_objects()

        model: Small_LLM_Model = Small_LLM_Model()

        dict_result: str = '{\n"prompt": "' + f'{input_prompt}",\n"name": "'

        logits: List[float] = model.get_logits_from_input_ids(model.encode(llm_prompt)[0].tolist())
        next_token_id = int(np.argmax(logits))
        dict_result += model.decode(next_token_id) + '",\n"parameters": {"'

        
        return ""
    except Exception:
        sys.stderr.write("\033[91m")
        traceback.print_exc()
        sys.stdout.write("\033[0m")
