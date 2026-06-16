from enum import Enum, auto
from llm_sdk import Small_LLM_Model
import numpy as np
from torch import Tensor


class States(Enum):
    """States for constrained decoding"""
    OPEN_SQUARE_BRACKETS = auto()

    # CLOSE_SQUARE_BRACKETS = auto()


def constrain_decoding(llm_prompt: str) -> str:
    """ Constrained Decoding """
    
