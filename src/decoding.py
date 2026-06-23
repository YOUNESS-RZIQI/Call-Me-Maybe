from llm_sdk import Small_LLM_Model
import numpy as np
from typing import List
import sys
import traceback
import json
from src.models import DefinitionValidator
from src.parser import Parser


model: Small_LLM_Model = Small_LLM_Model()


def args_decoding(vc: dict, llm_prompt: str, dict_result: str, key_index: int,
                  keys: List[str], ky_type: List[str]) -> tuple:
    """ Decodes arguments for a specific function call """

    dict_result += '"' + keys[key_index] + '": '
    llm_prompt += '"' + keys[key_index] + '": '

    if ky_type[key_index] in ("number", "decimal", "float", "num", "n"):
        allowed_tokens_ids = {
            vc["0"], vc["1"], vc["2"], vc["3"], vc["4"], vc["5"],
            vc["6"], vc["7"], vc["8"], vc["9"], vc["."], vc[","],
            vc["-"], vc["+"]}

    elif ky_type[key_index] in ("int", "integer"):
        allowed_tokens_ids = {
            vc["0"], vc["1"], vc["2"], vc["3"], vc["4"], vc["5"],
            vc["6"], vc["7"], vc["8"], vc["9"], vc[","],
            vc["-"], vc["+"]}

    elif ky_type[key_index] in ("bool", "boolean"):
        allowed_tokens_ids = {vc["true"], vc["True"], vc["TRUE"],
                              vc["false"], vc["False"], vc["FALSE"],
                              vc[","]}

    elif ky_type[key_index] in ("string", "s", "str"):
        # FIX: We manually add the opening quote for string types.
        # This prevents the LLM from hallucinating numbers (like '1') because it
        # forces the LLM to realize it is inside a string value.
        dict_result += '"'
        llm_prompt += '"'
        allowed_tokens_ids = set(range(len(vc)))

    # '",\n"parameters": { "a": '

    while (1):
        logits: List[float] = model.get_logits_from_input_ids(
            model.encode(llm_prompt)[0].tolist())
        # masking the logits to only allow the allowed_tokens_ids.
        for index in range(0, len(logits)):
            if index not in allowed_tokens_ids:
                logits[index] = float("-inf")

        next_token_id = int(np.argmax(logits))

        # Decode the token into a string variable to avoid multiple decode calls
        decoded_token = model.decode([next_token_id])

        if ky_type[key_index] in ("string", "s", "str") and '"' in decoded_token:
            # The model finished the string by generating a closing quote.
            # Since this is an intermediate argument, we MUST end with a comma.
            token_to_add = decoded_token.replace("}", "")
            if "," not in token_to_add:
                token_to_add += ", "
            elif ", " not in token_to_add:
                token_to_add = token_to_add.replace(",", ", ")
            dict_result += token_to_add
            llm_prompt += token_to_add
            break

        if ky_type[key_index] not in ("string", "s", "str") and "," in decoded_token:
            # For numbers/bools, we stop when it generates a comma.
            decoded_token = decoded_token.replace(",", ", ")
            dict_result += decoded_token
            llm_prompt += decoded_token
            break

        dict_result += decoded_token
        llm_prompt += decoded_token
    return (llm_prompt, dict_result)


def constrain_decoding(llm_prompt: str, input_prompt: str) -> str:
    """ Constrained Decoding for JSON """
    try:

        dict_result: str = '{\n"prompt": "' + f'{input_prompt}",\n"name": "'
        function_number: str = ""
        vocab_path = model.get_path_to_vocab_file()
        with open(vocab_path, "r") as f:
            vc = json.load(f)

        # allowed tokens: 0 1 2 3 4 5 6 7 8 9 . ,
        allowed_tokens_ids = {
            vc["0"], vc["1"], vc["2"], vc["3"], vc["4"], vc["5"],
            vc["6"], vc["7"], vc["8"], vc["9"], vc["."], vc[","],
            vc["-"], vc["+"]
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
        dict_result += '",\n"parameters": { '

        chosen_func_obj: DefinitionValidator = None
        for func in functions_def_obj:
            if func.name == functions_def_list[int(function_number)]:
                chosen_func_obj = func
                break

        keys: List[str] = []
        for key in chosen_func_obj.parameters.keys():
            keys.append(key)

        ky_type: List[str] = []
        for value in chosen_func_obj.parameters.values():
            ky_type.append(value.type)

        llm_prompt += dict_result

        # i will do all the args until the last one and i will stop, and also i stop at comma ','
        for key_index in range(0, len(keys) - 1):
            llm_prompt, dict_result = args_decoding(vc,
                                                    llm_prompt,
                                                    dict_result,
                                                    key_index,
                                                    keys,
                                                    ky_type)

        # last arg:

        last_key_index: int = len(keys) - 1
        dict_result += '"' + keys[last_key_index] + '": '
        llm_prompt += '"' + keys[last_key_index] + '": '

        if ky_type[last_key_index] in ("number", "decimal", "float", "num", "n"):
            # We add back vc[","] so the model doesn't infinite loop if it strongly prefers a comma
            # to end the number. We will catch the comma and replace it with '}'.
            allowed_tokens_ids = {
                vc["0"], vc["1"], vc["2"], vc["3"], vc["4"], vc["5"],
                vc["6"], vc["7"], vc["8"], vc["9"], vc["."], vc["}"],
                vc["-"], vc["+"], vc[","]}

        if ky_type[last_key_index] in ("int", "integer"):
            allowed_tokens_ids = {
                vc["0"], vc["1"], vc["2"], vc["3"], vc["4"], vc["5"],
                vc["6"], vc["7"], vc["8"], vc["9"], vc["}"],
                vc["-"], vc["+"], vc[","]}

        if ky_type[last_key_index] in ("bool", "boolean"):
            allowed_tokens_ids = {vc["true"], vc["True"], vc["TRUE"],
                                  vc["false"], vc["False"], vc["FALSE"],
                                  vc["}"], vc[","]}

        if ky_type[last_key_index] in ("string", "s", "str"):
            # FIX: We manually add the opening quote for string types.
            # This forces the LLM to generate the text content instead of a random number.
            dict_result += '"'
            llm_prompt += '"'
            allowed_tokens_ids = set(range(len(vc)))

        # '",\n"parameters": { "a": '

        while (1):
            logits: List[float] = model.get_logits_from_input_ids(
                model.encode(llm_prompt)[0].tolist())
            # masking the logits to only allow the allowed_tokens_ids.
            for index in range(0, len(logits)):
                if index not in allowed_tokens_ids:
                    logits[index] = float("-inf")

            next_token_id = int(np.argmax(logits))

            # Decode the token into a string variable
            decoded_token = model.decode([next_token_id])

            if ky_type[last_key_index] in ("string", "s", "str") and '"' in decoded_token:
                # The model finished the final string. We MUST end with a closing brace.
                token_to_add = decoded_token.replace(",", "")
                if "}" not in token_to_add:
                    token_to_add += "}"
                dict_result += token_to_add
                llm_prompt += token_to_add
                break

            if ky_type[last_key_index] not in ("string", "s", "str"):
                if "}" in decoded_token:
                    dict_result += decoded_token
                    llm_prompt += decoded_token
                    break
                if "," in decoded_token:
                    # If the model generated a comma instead of a brace (common for numbers/bools)
                    # we replace it with a brace because it's the final argument!
                    dict_result += decoded_token.replace(",", "}")
                    llm_prompt += decoded_token.replace(",", "}")
                    break

            dict_result += decoded_token
            llm_prompt += decoded_token

        dict_result += "\n}"

        print(dict_result, "\n\n")
        return dict_result
    except Exception:
        sys.stderr.write("\033[91m")
        traceback.print_exc()
        sys.stdout.write("\033[0m")
