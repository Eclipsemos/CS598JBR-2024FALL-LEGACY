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
    return None, None

def generate_prompt(inputs, problem, solution):
    """Generate a new prompt based on inputs and program."""
    prompt = f"""You are an AI programming assistant, utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.
### Instruction:
Given the following programming problem and its canonical_solution,
If the input of this program is {inputs}, what will the following code return after executing?
The return value prediction must be enclosed between [Output] and [/Output] tags. For example : [Output]result[/Output].
Remeber you ONLY return [Output]result[/Output] where result is the your prediciton result.
programming problem:
{problem}

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

            if inputs and expected_output:
                # Generate the prompt
                prompt = generate_prompt(inputs, data["prompt"], data["canonical_solution"])

                # Create the new formatted JSON object
                new_data = {
                    "task_id": data["task_id"],
                    "prompt": prompt,
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

    # Run the script to reformat the JSONL file
    reformat_jsonl(input_file, output_file)
