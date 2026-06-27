*This project has been created as part of the 42 curriculum by yrziqi.*

# Call Me Maybe - Introduction to function calling in LLMs

## Description
This project focuses on building a function calling tool that acts as an intermediary between a Small Language Model (SLM) and structured, machine-executable function calls. Rather than allowing the LLM to respond to user prompts naturally (which can lead to malformed outputs), this system translates natural language queries into exact function definitions and parameters using **Constrained Decoding**.

The primary goal is to ensure that the AI model produces 100% syntactically correct and schema-compliant JSON outputs, making the outputs reliable and executable.

## Instructions
### Prerequisites
- Python 3.10+
- `uv` package manager installed

### Installation & Execution
You can use the provided `Makefile` to install dependencies and run the project:

```bash
# Install dependencies
make install

# Run the pipeline
make run
```

Alternatively, you can run it manually via `uv`:

```bash
uv run python -m src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calls.json
```

## Algorithm Explanation
The solution uses **Constrained Decoding** to guarantee that the Large Language Model's output adheres to a strict JSON format defined by the provided schemas.

1. **Prompt Construction**: The tool first formats the function definitions alongside the user prompt into a context window the LLM can understand.
2. **Step-by-Step Decoding**: Instead of letting the model freely generate the complete response, token generation is intercepted at every step.
3. **Logit Masking**: Based on the current parsing state (e.g., if we expect a number, boolean, or string), the tool calculates the valid tokens allowed for the next step. It accesses the vocabulary mappings and sets the logits (probabilities) of invalid tokens to negative infinity (`-inf`).
4. **Token Selection**: The model then selects the highest probability token out of the *allowed* pool of tokens, guaranteeing that every generated token contributes to a valid JSON structure.
5. **Type Casting**: After generation, the tool casts numerical fields into proper Python floats according to the schema before serializing the final result.

## Design Decisions
- **Token-by-Token Validation**: I elected to enforce JSON constraints at the token level using logit modification. This bypasses the SLM's natural unreliability with strict formats and turns generating JSON into a deterministic, guided process.
- **Dynamic Prefix Generation**: Strings are given an enforced opening quote (`"`) before the LLM generates tokens. This serves as a strong hint to the LLM to avoid generating number characters for string fields, preventing common hallucinations.
- **Pydantic Models**: Used for rigorous internal state validation when parsing the initial definitions and requests, guaranteeing internal structure correctness before reaching the LLM.

## Performance Analysis
- **Accuracy**: By explicitly modifying logit arrays to negative infinity for schema-violating tokens, the syntactic error rate drops to effectively 0%.
- **Speed**: The system's processing speed directly correlates with the SLM's generation throughput. Running inference on CPU for a 0.6B parameter model generates outputs relatively fast, completing test batches comfortably under the required threshold.
- **Reliability**: The system is highly robust because it treats token generation as a finite state machine; it will not let the model generate invalid commas, misplaced quotes, or incorrect types.

## Challenges Faced
- **Token Redefinitions (Flake8/Mypy)**: Overlapping type annotations inside constrained blocks led to mypy redefinition errors. This was solved by declaring the `Set[int]` type initially and rebinding standard dictionary updates later in the flow.
- **Escaping Quotes in Prompts**: User prompts containing double quotes (e.g. `"Hello"`) would break the outer JSON structure being generated. By using `json.dumps()` for the prompt input, strings were properly escaped before passing to the state builder.
- **Infinite Generation Loops**: The SLM could occasionally enter an infinite loop when generating integers (like appending numbers indefinitely). To solve this, a hard cap on digits was placed based on the function list size, forcefully halting generation.

## Testing Strategy
- Validated output strictly against `functions_definition.json` schema requirements.
- Checked edge cases involving embedded string characters, empty arguments, and overlapping argument types.
- Leveraged `flake8` and `mypy` statically to find resource leaks, unused imports, or bad typing before runtime.

## Resources
- [Qwen 0.6B Model Documentation](https://huggingface.co/Qwen)
- JSON state machine tracking principles
- AI utilized throughout learning: Discussed structural constraints of LLM decoders and utilized LLMs to suggest edge-case testing methodologies during development.

## Example Usage
**Input Prompt**: `"Reverse the string 'hello'"`

**Terminal Output Log**:
```json
{
"prompt": "Reverse the string 'hello'",
"name": "fn_reverse_string",
"parameters": {
"s": "hello"
}
}
```
