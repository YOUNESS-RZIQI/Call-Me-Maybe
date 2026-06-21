from llm_sdk import Small_LLM_Model
import numpy as np
from typing import List
import sys
import traceback
import json
from src.models import DefinitionValidator
from src.parser import Parser


def constrain_decoding(llm_prompt: str, input_prompt: str) -> str:
    """ Constrained Decoding for JSON """
    try:
        model: Small_LLM_Model = Small_LLM_Model()
        dict_result: str = '{\n"prompt": "' + f'{input_prompt}",\n"name": "'
        function_number: str = ""
        vocab_path = model.get_path_to_vocab_file()
        with open(vocab_path, "r") as f:
            vc = json.load(f)

        # allowed tokens: 0 1 2 3 4 5 6 7 8 9 . ,
        allowed_tokens_ids = {
            vc["0"], vc["1"], vc["2"], vc["3"], vc["4"], vc["5"],
            vc["6"], vc["7"], vc["8"], vc["9"], vc["."], vc[","]
        }

        functions_def_obj: List[
            DefinitionValidator] = Parser.get_input_definitions_objects()

        functions_def_list: List[str] = []
        for obj in functions_def_obj:
            functions_def_list.append(obj.name)

        while (1):
            logits: List[float] = model.get_logits_from_input_ids(
                model.encode(llm_prompt + function_number)[0].tolist())
            # masking the logits to only allow digits from 0-9 and comma and dot.
            for index in range(0, len(logits)):
                if index not in allowed_tokens_ids:
                    logits[index] = float("-inf")

            next_token_id = int(np.argmax(logits))
            if not (model.decode([next_token_id]).isdigit()):
                break
            function_number += model.decode(next_token_id)

        dict_result += functions_def_list[int(function_number)]
        dict_result += '",\n"parameters": '

        # chosen_func_obj: DefinitionValidator = None
        # for func in functions_def_obj:
        #     if func.name == functions_def_list[int(function_number)]:
        #         chosen_func_obj = func
        #         break

        args_llm_prompt: str = 'Example of Expected result: Example start afters colon:{\n"prompt": "What is the sum of 2 and 3?",\n"name": "fn_add_numbers",\n"parameters": {"a": 2, "b": 3}End of Example. Complet my solution which will start after colon :'

        while (1):
            logits: List[float] = model.get_logits_from_input_ids(
                model.encode(args_llm_prompt + dict_result)[0].tolist())
            next_token_id = int(np.argmax(logits))

            if "}" in model.decode([next_token_id]):
                dict_result += model.decode([next_token_id])
                break
            dict_result += model.decode([next_token_id])
        
        print(dict_result, "")
        # print(functions_def_obj[int(function_number)].parameters[0].type)
        # print(llm_prompt, "\n\n")
        # print(function_number, "\n\n")
        # print(functions_def_list[int(function_number)], "\n\n")
        # print(functions_def_list, "\n\n")
        # print(dict_result)
        return dict_result
    except Exception:
        sys.stderr.write("\033[91m")
        traceback.print_exc()
        sys.stdout.write("\033[0m")
