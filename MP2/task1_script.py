import json
import re
import sys

def extract_inputs_and_expected(test_code):
    """Extract the input and expected output from the first assert statement in the test function."""
    lines = test_code.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("assert candidate("):
            # Use regex to extract the input and expected value
            match = re.match(r"assert candidate\((.*)\) == (.*)", line)
            if match:
                input_str = match.group(1)
                expected_output = match.group(2)
                return input_str, expected_output
    return None, True

def van_generate_prompt(inputs, problem, solution):
    """Generate a new prompt based on inputs and program."""
    prompt = f"""You are an AI programming assistant, utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.
### Instruction:
Given the following programming problem and its canonical_solution,
If the input of this program is {inputs}, what will the following code return after executing?
The return value prediction must be enclosed between [Output] and [/Output] tags. For example : [Output]result[/Output].
REMEBER YOU ONLY and MUST RETURN [Output]result[/Output] in ### Response section!!! result is the output of program.
AND ATTENTION, the "result" is the returned value of the program, NOT ANY OTHER THINGS!!
programming problem:
{problem}

canonical_solution:
{solution}
### Response:
"""
    return prompt

def craft_generate_prompt(inputs, problem, solution):
    prompt = f"""You are tasked with solving a programming problem by predicting the output of a given canonical solution based on specified inputs. Follow these steps to ensure the accuracy and clarity of your answer:
1. Understand the Problem: Carefully read the programming problem and what the code is intended to solve.
2. Analyze the Code: Break down the provided canonical solution into several necessary logical parts to understand each component’s role in achieving the solution.
3. Simulate the Code Execution: Reason the code with the given inputs, carefully tracing the values and operations to understand how the output is derived.
4. Document Each Step: Clearly describe your thoughts  and the reasoning behind each code execution step, including any intermediate results that lead to the final output.
5. Present the Final Output: Combining all insights to determine the final result after thoroughly reasoning through and simulating the code.
Each step of your reasoning SHOULD BE well-documented, providing a clear explanation of your thought process and any intermediate results.
The final output of the program, after executing with the given inputs, should be presented and enclosed within [Output] and [/Output] tags. For example:
- Step 1: [Describe the initial state and setup based on the problem requirements].
- Step 2: [Explain the logic of the first part of the code and how it manipulates the input].
- ...
- Final Step: [Summarize and present the computed result as the answer, enclosed in the tags].
Example:
- Step 1: [The problem requires sorting a list of integers in descending order. The input list is [3, 1, 4, 1, 5].]
- Step 2: [The canonical solution uses a sorting function. It will rearrange the integers in descending order based on their values.]
- ...
- Final Step: [Output]5, 4, 3, 1, 1[/Output]

Now, let's do it.
Here is the programming problem:


programming problem:
{problem}

programming input:
{inputs}

canonical_solution:
{solution}
### Response:
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

            if inputs:
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
