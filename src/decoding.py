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
            if not (model.decode(next_token_id).isdigit()):
                break
            function_number += model.decode(next_token_id)

        dict_result += functions_def_list[int(function_number)]
        dict_result += '",\n"parameters": {'

        llm_context = llm_prompt + function_number + '",\n"parameters": {'
        
        parameters_dict = functions_def_obj[int(function_number)].parameters
        keys = list(parameters_dict.keys())
        
        for i, key in enumerate(keys):
            param_type = parameters_dict[key].type
            
            key_str = f'"{key}": '
            if param_type == 'string':
                key_str += '"'
            
            dict_result += key_str
            llm_context += key_str
            
            value_str = ""
            while True:
                logits: List[float] = model.get_logits_from_input_ids(
                    model.encode(llm_context + value_str)[0].tolist())
                
                if param_type == 'number':
                    for index in range(len(logits)):
                        if index not in allowed_tokens_ids:
                            logits[index] = float("-inf")
                            
                next_token_id = int(np.argmax(logits))
                decoded_char = model.decode(next_token_id)
                
                if param_type == 'number':
                    if not (decoded_char.isdigit() or decoded_char == '.'):
                        break
                    value_str += decoded_char
                elif param_type == 'string':
                    if '"' in decoded_char:
                        quote_index = decoded_char.find('"')
                        if quote_index != -1:
                            value_str += decoded_char[:quote_index]
                            break
                    value_str += decoded_char

            if param_type == 'string':
                dict_result += value_str + '"'
                llm_context += value_str + '"'
            else:
                dict_result += value_str
                llm_context += value_str

            if i < len(keys) - 1:
                dict_result += ", "
                llm_context += ", "
        
        dict_result += "}\n}"
        
        return dict_result
    except Exception:
        sys.stderr.write("\033[91m")
        traceback.print_exc()
        sys.stdout.write("\033[0m")
