import json
import re
import sys


def van_generate_prompt(problem, solution):
    """Generate a new prompt based on inputs and program."""
    prompt = f"""You are an AI programming assistant. You are an AI programming assistant, utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.

### Instruction:

Generate a pytest test suite for the following code.
Each test should be a single function.
Only write unit tests in the output and nothing else.
{problem}
{solution}
### Response:
"""
    return prompt

def craft_generate_prompt(problem, solution):
    prompt = f"""You are an AI programming assistant. You are an AI programming assistant, utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.

### Instruction:

Generate a pytest test suite for the following code.
Each test should be a single function.
Use Chain of Thoughts
Only write unit tests in the output and nothing else.
{problem}
{solution}
### Response:
"""
    return prompt

def reformat_jsonl(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            # Load the JSON object from the original JSONL line
            data = json.loads(line)
            # Generate the prompt
            van_prompt = van_generate_prompt( data["prompt"], data["canonical_solution"])
            crafted_prompt = craft_generate_prompt(data["prompt"], data["canonical_solution"])
            # Create the new formatted JSON object
            program = data["prompt"] + "\n" + data["canonical_solution"]
            new_data = {
                "task_id": data["task_id"],
                "vanilla_prompt": van_prompt,
                "crafted_prompt": crafted_prompt,
                "program":  program
            }
            # print(data["task_id"] + " " + expected_output)
            # Write the new JSONL object to the output file
            json.dump(new_data, f_out)
            f_out.write("\n")

if __name__ == "__main__":
    args = sys.argv[1:]
    input_file = args[0]
    output_file = args[1]
    print("INPUT: " + input_file)
    print("OUTPUT: " + output_file)
    # Run the script to reformat the JSONL file
    reformat_jsonl(input_file, output_file)
