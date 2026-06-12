import argparse
import json
import os
import traceback

from src.parser import Parser
from src.builder import PromptBuilder
from src.decoder import ConstrainedDecoder
from llm_sdk.llm_sdk import Small_LLM_Model

def main() -> None:
    parser = argparse.ArgumentParser(description="Function Calling CLI")
    parser.add_argument("--functions_definition", type=str, default="data/input/functions_definition.json")
    parser.add_argument("--input", type=str, default="data/input/function_calling_tests.json")
    parser.add_argument("--output", type=str, default="data/output/function_calling_results.json")
    
    args = parser.parse_args()
    
    try:
        definitions = Parser.get_input_definitions_objects(args.functions_definition)
        if not definitions:
            raise ValueError("Could not parse function definitions")
            
        prompts = Parser.get_input_prompts_as_list_of_strs(args.input)
        if not prompts:
            raise ValueError("Could not parse input prompts")
            
        llm = Small_LLM_Model("Qwen/Qwen3-0.6B")
        decoder = ConstrainedDecoder(llm, definitions)
        
        results = []
        for prompt_str in prompts:
            context_prompt = PromptBuilder.build_final_prompt_string(prompt_str, definitions)
            json_str = decoder.decode(context_prompt)
            
            try:
                parsed_json = json.loads(json_str)
            except json.JSONDecodeError:
                parsed_json = {"name": "error", "parameters": {}}
                
            results.append({
                "prompt": prompt_str,
                "name": parsed_json.get("name"),
                "parameters": parsed_json.get("parameters", {})
            })
            
        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            
        with open(args.output, "w") as f:
            json.dump(results, f, indent=4)
            
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    main()
