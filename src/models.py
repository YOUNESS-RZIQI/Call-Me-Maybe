from pydantic import BaseModel
from typing import Dict


class PromptValidator(BaseModel):
    """ Prompt Input Validator """
    prompt: str


class TypeDefinition(BaseModel):
    type: str


class DefinitionValidator(BaseModel):
    """ Definition Input Validator """
    name: str
    description: str
    parameters: Dict[str, TypeDefinition]
    returns: TypeDefinition
