from src.parser import Parser
from src.builder import PromptBuilder


print(PromptBuilder.build_final_prompt_string("What is the sum of 2 and 3?", Parser.get_input_definitions_objects()))