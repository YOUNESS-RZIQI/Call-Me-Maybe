from enum import Enum, auto
from llm_sdk import Small_LLM_Model
import numpy as np
from typing import List, Dict
import sys
import traceback
from src.models import DefinitionValidator



def constrain_decoding(llm_prompt: str, input_prompt: str, functions_def_list: List[str]) -> str:
    """ Constrained Decoding for JSON """
    try:
        model: Small_LLM_Model = Small_LLM_Model()
        dict_result: str = '{\n"prompt": "' + f'{input_prompt}",\n"name": "'

        function_number: str = ""

        while (1):
            logits: List[float] = model.get_logits_from_input_ids(model.encode(llm_prompt + function_number)[0].tolist())
            next_token_id = int(np.argmax(logits))
            if not (model.decode(next_token_id).isdigit()):
                break
            function_number += model.decode(next_token_id)
        #check that the number nout out side of the list " unknown function name"
        if int(function_number) >= len(functions_def_list):
            dict_result += " unknown function call"
        else:
            dict_result += functions_def_list[int(function_number)]
        dict_result += '",\n"parameters": {"a": '

        print(dict_result, "\n\n")

        return ""
    except Exception:
        sys.stderr.write("\033[91m")
        traceback.print_exc()
        sys.stdout.write("\033[0m")
