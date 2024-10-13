# {"task_id": "HumanEval/10", "prompt": "\n\ndef is_palindrome(string: str) -> bool:\n    \"\"\" Test if given string is a palindrome \"\"\"\n    return string == string[::-1]\n\n\ndef make_palindrome(string: str) -> str:\n    \"\"\" Find the shortest palindrome that begins with a supplied string.\n    Algorithm idea is simple:\n    - Find the longest postfix of supplied string that is a palindrome.\n    - Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.\n    >>> make_palindrome('')\n    ''\n    >>> make_palindrome('cat')\n    'catac'\n    >>> make_palindrome('cata')\n    'catac'\n    \"\"\"\n", "canonical_solution": "    if not string:\n        return ''\n\n    beginning_of_suffix = 0\n\n    while not is_palindrome(string[beginning_of_suffix:]):\n        beginning_of_suffix += 1\n\n    return string + string[:beginning_of_suffix][::-1]\n", "test": "\n\nMETADATA = {\n    'author': 'jt',\n    'dataset': 'test'\n}\n\n\ndef check(candidate):\n    assert candidate('') == ''\n    assert candidate('x') == 'x'\n    assert candidate('xyz') == 'xyzyx'\n    assert candidate('xyx') == 'xyx'\n    assert candidate('jerry') == 'jerryrrej'\n", "entry_point": "make_palindrome"}
# read jsonl fetch "can_sol" and first assertion in the "test"
# generate prompt message
# format as purple content
# write into a new jsonl 
# {"task_id": ,"prompt": , "expect": , "is_correct": } 
# expected is output of the can_sol functions' return

# prompt model

# compare acc rate



import json
import re

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

def generate_prompt(inputs, program):
    """Generate a new prompt based on inputs and program."""
    prompt = f"""You are an AI programming assistant, utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.
### Instruction:
If the string is {inputs}, what will the following code return?
The return value prediction must be enclosed between [Output] and [/Output] tags. For example : [Output]prediction[/Output].

{program}

### Response:
"""
    return prompt

def reformat_jsonl(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            # Load the JSON object from the original JSONL line
            data = json.loads(line)

            # Extract the program and inputs
            program = data["canonical_solution"]
            test_code = data["test"]
            inputs, expected_output = extract_inputs_and_expected(test_code)

            # Generate the prompt
            prompt = generate_prompt(inputs, program)

            # Create the new formatted JSON object
            new_data = {
                "task_id": data["task_id"],
                "prompt": prompt,
                "expect": f"[Output]{expected_output}[/Output]",
                "is_correct": None
            }

            # Write the new JSONL object to the output file
            json.dump(new_data, f_out)
            f_out.write("\n")

# Specify the input and output file paths
input_file = "selected_humaneval_171768020378419351865442221048553552766.jsonl"
output_file = "task_1_171768020378419351865442221048553552766_vanilla.jsonl"

# Run the script to reformat the JSONL file
reformat_jsonl(input_file, output_file)
