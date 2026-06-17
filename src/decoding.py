from enum import Enum, auto
from llm_sdk import Small_LLM_Model
import numpy as np
from typing import List


class States(Enum):
    """States for constrained decoding"""
    OPEN_SQUARE_BRACKETS = auto()

    # CLOSE_SQUARE_BRACKETS = auto()


def constrain_decoding(llm_prompt: str) -> str:
    """ Constrained Decoding """
    model: Small_LLM_Model = Small_LLM_Model()

    logits: List[int] = model.get_logits_from_input_ids(model.encode(llm_prompt)[0].tolist())

    num: int = 0
    for logit in logits:
        if model.decode([logit]) != "[":
            logits[num] = float('-inf')
        num += 1
    print(model.decode([int(np.argmax(logits))]), "\n\n")
