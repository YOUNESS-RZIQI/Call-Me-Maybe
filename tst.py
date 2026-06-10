import pydantic_core
dict_list = {
        "name": "youness",
        "descreption": "1337 student (42 network) + Programming Advices Student",
        "Parametters": {
            "a": {"Type": "number"},
            "b": {"Type": "number"}
        },
        "age": "21"
}


# pyrefly: ignore [missing-import]
# from pydantic import BaseModel
# from typing import Dict


# class TypeDefinition(BaseModel):
#     type: str


# class DefinitionValidator(BaseModel):
#     """ Definition Input Validator """
#     name: str
#     description: str
#     parameters: Dict[str, TypeDefinition]
#     returns: TypeDefinition


# result = DefinitionValidator(
#     name="youness",
#     description="1337 student (42 network) + Programming Advices Student",
#     parameters={
#         "a": TypeDefinition(type="number"),
#         "b": TypeDefinition(type="number")
#     },
#     returns=TypeDefinition(type="number")
# )

# print(result.name)


print(**dict_list)