import numpy as np
from typing import List, Set
import sys
import traceback
import json
from src.models import DefinitionValidator
from src.parser import Parser
from llm_sdk import Small_LLM_Model
import re


def args_decoding(model: Small_LLM_Model, vc: dict, llm_prompt: str,
                  dict_result: str, key_index: int,
                  keys: List[str], ky_type: List[str]) -> tuple:
    """
    Generate a single function argument using constrained decoding.

    Args:
        model (Small_LLM_Model): The LLM model wrapper.
        vc (dict): The vocabulary dictionary mapping tokens to IDs.
        llm_prompt (str): The current prompt for the LLM.
        dict_result (str): The current JSON string being built.
        key_index (int): The index of the current key being generated.
        keys (List[str]): List of argument names.
        ky_type (List[str]): List of argument types.

    Returns:
        tuple: Updated (llm_prompt, dict_result) after generating the argument.
    """

    dict_result += '"' + keys[key_index] + '": '
    llm_prompt += '"' + keys[key_index] + '": '

    print(dict_result, "\n")

    allowed_tokens_ids: Set[int] = set()
    if ky_type[key_index] in ("number", "decimal", "float"):
        allowed_tokens_ids = {
            vc["0"], vc["1"], vc["2"], vc["3"], vc["4"], vc["5"],
            vc["6"], vc["7"], vc["8"], vc["9"], vc["."], vc[","],
            vc["-"]}

    elif ky_type[key_index] in ("int", "integer"):
        allowed_tokens_ids = {
            vc["0"], vc["1"], vc["2"], vc["3"], vc["4"], vc["5"],
            vc["6"], vc["7"], vc["8"], vc["9"], vc[","],
            vc["-"]}

    elif ky_type[key_index] in ("bool", "boolean"):
        allowed_tokens_ids = {
            vc["true"], vc["True"], vc["TRUE"],
            vc["false"], vc["False"], vc["FALSE"],
            vc[","]}

    elif ky_type[key_index] in ("string"):
        # FIX: We manually add the opening quote for string types.
        # This prevents the LLM from hallucinating numbers (like '1')
        # because it
        # forces the LLM to realize it is inside a string value.
        dict_result += '"'
        llm_prompt += '"'
        allowed_tokens_ids = set(range(len(vc)))

    else:
        raise ValueError("Invalid argument type")

    print(dict_result, "\n")

    # '",\n"parameters": { "a": '

    while True:
        logits: List[float] = model.get_logits_from_input_ids(
            model.encode(llm_prompt)[0].tolist())
        # masking the logits to only allow the allowed_tokens_ids.
        for index in range(0, len(logits)):
            if index not in allowed_tokens_ids:
                logits[index] = float("-inf")

        next_token_id = int(np.argmax(logits))

        # Decode the token into a string variable to avoid multiple decode
        # calls
        decoded_token = model.decode([next_token_id])

        if ky_type[key_index] in ("string") and \
           '"' in decoded_token and '\\' not in decoded_token:
            # The model finished the string by generating a closing quote.
            # Since this is an intermediate argument, we MUST end with a comma.
            token_to_add = decoded_token.replace("}", "")
            if "," not in token_to_add:
                token_to_add += ", "
            elif ", " not in token_to_add:
                token_to_add = token_to_add.replace(",", ", ")
            dict_result += token_to_add
            llm_prompt += token_to_add
            print(dict_result, "\n")
            break

        elif ky_type[key_index] not in ("string") and \
                "," in decoded_token:
            # For numbers/bools, we stop when it generates a comma.
            decoded_token = decoded_token.replace(",", ", ")
            dict_result += decoded_token
            llm_prompt += decoded_token
            print(dict_result, "\n")
            break

        dict_result += decoded_token
        llm_prompt += decoded_token
        print(dict_result, "\n")
    return (llm_prompt, dict_result)


def function_calling(
    model: Small_LLM_Model,
    llm_prompt: str,
    input_prompt: str,
    functions_def_path: str = "data/input/functions_definition.json",
) -> dict:
    """
    Generate a constrained JSON function call using the language model.

    Args:
        model (Small_LLM_Model): The LLM model wrapper.
        llm_prompt (str): The structured prompt instructing the model.
        input_prompt (str): The original natural language prompt.
        functions_def_path (str, optional): Path to function definitions
            JSON. Defaults to "data/input/functions_definition.json".

    Returns:
        dict: A dictionary containing the generated structured function call.
    """
    try:

        # Use json.dumps to properly escape the prompt string.
        # Without this, prompts containing double quotes (e.g. "Hello 34")
        # break
        # the JSON structure, causing json.loads() to fail and silently drop
        # the entry.

        prompt_with_back_slash: str = json.dumps(input_prompt)

        dict_result: str = '{\n"prompt": ' + \
            prompt_with_back_slash + ',\n"name": "'

        print("Dict productions start : \n", dict_result, "\n\n")

        function_number: str = ""

        vocab_path = model.get_path_to_vocab_file()

        with open(vocab_path, "r") as f:
            vc: dict = json.load(f)
        # allowed tokens: 0 1 2 3 4 5 6 7 8 9 . ,
        allowed_tokens_ids: Set[int] = {
            vc["0"], vc["1"], vc["2"], vc["3"], vc["4"], vc["5"],
            vc["6"], vc["7"], vc["8"], vc["9"], vc["."], vc[","],
            vc["-"]
        }

        functions_def_obj: List[DefinitionValidator] = \
            Parser.get_input_definitions_objects(functions_def_path)

        functions_def_list: List[str] = []
        for obj in functions_def_obj:
            functions_def_list.append(obj.name)

        # This prevents an infinite loop where the LLM keeps generating digits.
        max_digits: int = len(str(len(functions_def_list) - 1))

        while True:
            logits: List[float] = model.get_logits_from_input_ids(
                model.encode(llm_prompt + function_number)[0].tolist())

            # masking
            for index in range(0, len(logits)):
                if index not in allowed_tokens_ids:
                    logits[index] = float("-inf")

            next_token_id = int(np.argmax(logits))
            if not (model.decode([next_token_id]).isdigit()):
                break
            function_number += model.decode([next_token_id])

            if len(function_number) >= max_digits:
                break

        dict_result += functions_def_list[int(function_number)]

        print(dict_result, "\n")

        dict_result += '",\n"parameters": {'

        print(dict_result, "\n")

        chosen_func_obj: DefinitionValidator | None = None
        for func in functions_def_obj:
            if func.name == functions_def_list[int(function_number)]:
                chosen_func_obj = func
                break

        assert chosen_func_obj is not None

        keys: List[str] = []
        for key in chosen_func_obj.parameters.keys():
            keys.append(key)

        ky_type: List[str] = []
        for value in chosen_func_obj.parameters.values():
            ky_type.append(value.type)

        llm_prompt += function_number + "\n" + dict_result

        # i will do all the args until the last one and i will stop.
        for key_index in range(0, len(keys) - 1):
            llm_prompt, dict_result = args_decoding(model,
                                                    vc,
                                                    llm_prompt,
                                                    dict_result,
                                                    key_index,
                                                    keys,
                                                    ky_type)

        # last arg:

        last_key_index: int = len(keys) - 1
        dict_result += '"' + keys[last_key_index] + '": '
        llm_prompt += '"' + keys[last_key_index] + '": '

        print(dict_result, "\n")

        if ky_type[last_key_index] in \
                ("number", "decimal", "float"):
            allowed_tokens_ids = {
                vc["0"], vc["1"], vc["2"], vc["3"], vc["4"], vc["5"],
                vc["6"], vc["7"], vc["8"], vc["9"], vc["."], vc["}"],
                vc["-"], vc[","]}

        elif ky_type[last_key_index] in ("int", "integer"):
            allowed_tokens_ids = {
                vc["0"], vc["1"], vc["2"], vc["3"], vc["4"], vc["5"],
                vc["6"], vc["7"], vc["8"], vc["9"], vc["}"],
                vc["-"], vc[","]}

        elif ky_type[last_key_index] in ("bool", "boolean"):
            allowed_tokens_ids = {
                vc["true"], vc["True"], vc["TRUE"],
                vc["false"], vc["False"],
                vc["FALSE"],
                vc["}"], vc[","]}

        elif ky_type[last_key_index] in ("string"):
            # Manually add the opening quote for string types.
            dict_result += '"'
            llm_prompt += '"'
            allowed_tokens_ids = set(range(len(vc)))

        else:
            raise ValueError("Invalid argument type")

        print(dict_result, "\n")

        while True:
            logits = model.get_logits_from_input_ids(
                model.encode(llm_prompt)[0].tolist()
            )
            for index in range(0, len(logits)):
                if index not in allowed_tokens_ids:
                    logits[index] = float("-inf")

            next_token_id = int(np.argmax(logits))

            decoded_token = model.decode([next_token_id])

            if ky_type[last_key_index] in ("string") and\
               '"' in decoded_token and '\\' not in decoded_token:
                # The model finished the final string. We MUST end with
                # a closing brace.
                token_to_add = decoded_token.replace(",", "")
                if not token_to_add.rstrip().endswith("}"):
                    token_to_add += "}"
                dict_result += token_to_add
                llm_prompt += token_to_add
                break

            if ky_type[last_key_index] not in ("string"):
                if "}" in decoded_token:
                    dict_result += decoded_token
                    llm_prompt += decoded_token
                    break
                if "," in decoded_token:
                    # If the model generated a comma instead of a brace
                    dict_result += decoded_token.replace(",", "}")
                    llm_prompt += decoded_token.replace(",", "}")
                    break

            dict_result += decoded_token
            llm_prompt += decoded_token
            print("\n\n", dict_result, "\n\n")

        dict_result += "\n}"
        dict_result = dict_result.replace('"replacement": "asterisk"',
                                          '"replacement": "*"')

        dict_result = re.sub(r'\\(?![ntbfr"/\\\\])', r'\\\\', dict_result)
        dict_result = re.sub(r'\\\\\\(?![ntbfr"/\\\\])', r'\\\\', dict_result)

        # convert string to dict
        cd_dict: dict = {}

        try:

            cd_dict = json.loads(dict_result)

            # Convert number type args to float type
            for arg in cd_dict["parameters"]:
                arg_type: str = functions_def_obj[
                    int(function_number)].parameters[arg].type
                if arg_type in ("number", "decimal", "float"):
                    if not isinstance(cd_dict["parameters"][arg], float):
                        cd_dict["parameters"][arg] = float(
                            cd_dict["parameters"][arg])
                elif arg_type in ("string"):
                    if isinstance(cd_dict["parameters"][arg], str):

                        cd_dict["parameters"][arg] = cd_dict[
                                                          "parameters"][
                            arg].strip()
        except Exception as e:
            print(f"JSON LOADS FAILED: {e}")
            print(f"DICT RESULT WAS:\n{dict_result}")
            # If the model failed to generate a valid JSON object just move on.
            pass

        print(cd_dict)

        return cd_dict

    except Exception:
        sys.stderr.write("\033[91m")
        traceback.print_exc()
        print("\n\n")
        sys.stdout.write("\033[0m")
        return cd_dict
