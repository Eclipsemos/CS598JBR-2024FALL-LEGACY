import json
import re
import sys

# def extract_inputs_and_expected(test_code):
#     """Extract the input and expected output from the first assert statement in the test function."""
#     lines = test_code.split("\n")
#     for line in lines:
#         line = line.strip()
#         if line.startswith("assert candidate("):
#             # Use regex to extract the input and expected value
#             match = re.match(r"assert candidate\((.*)\) == (.*)", line)
#             if match:
#                 input_str = match.group(1)
#                 expected_output = match.group(2)
#                 return input_str, expected_output
#     return None, True

def extract_inputs_and_expected(test_code):
    """Extract the input and expected output from the test code."""
    lines = test_code.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("assert candidate("):
            match = re.match(r"assert\s+candidate\((.*)\)\s*==\s*(.*)", line)
            if match:
                input_str = match.group(1)
                expected_output = match.group(2)
                return input_str, expected_output
    return "", True

def van_generate_prompt(inputs, problem, solution):
    """Generate a new prompt based on inputs and program."""
    prompt = f"""You are an AI programming assistant, utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.
### Instruction:
Given the following program
If the input of this program is {inputs}, what will the following code return after executing?
The return value prediction must be enclosed between [Output] and [/Output] tags. For example : [Output]result[/Output].
REMEBER YOU ONLY and MUST RETURN [Output]result[/Output] in ### Response section!!! result is the output of program.
AND ATTENTION, the "result" is the returned value of the program, NOT ANY OTHER THINGS!!
program:
{problem}
{solution}
### Response:
"""
    return prompt

def craft_generate_prompt(inputs, problem, solution):
    prompt = f"""You are an AI programming assistant. Your task is to predict the output of the given program when executed with the specified inputs.

IMPORTANT:

- You MUST ONLY provide the final output of the program.
- The output must be enclosed between [Output] and [/Output] tags.
- Do NOT include any additional text, explanations, or reasoning.

For example, if the output is `42`, you should respond with:

[Output]42[/Output]

Here is the program:

{problem}
{solution}

Input:

{inputs}

Response:

"""
    return prompt

def reformat_jsonl(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            # Load the JSON object from the original JSONL line
            data = json.loads(line)

            # Extract the inputs, expected ouput
            test_code = data["test"]
            inputs, expected_output = extract_inputs_and_expected(test_code)

            # Generate the prompt
            van_prompt = van_generate_prompt(inputs, data["prompt"], data["canonical_solution"])
            crafted_prompt = craft_generate_prompt(inputs, data["prompt"], data["canonical_solution"])
            # Create the new formatted JSON object
            new_data = {
                "task_id": data["task_id"],
                "vanilla_prompt": van_prompt,
                "crafted_prompt": crafted_prompt,
                "expected": expected_output,
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
