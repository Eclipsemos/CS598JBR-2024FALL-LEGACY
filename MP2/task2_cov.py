import os
import subprocess
import json

def run_pytest_with_coverage(id):
    # Construct the command
    command = [
        'pytest',
        f'--cov=cov',
        f'--cov-report=json:Coverage/{id}_report.json',
        "cov_test.py"
    ]
    
    try:
        # Run the command using subprocess
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Print the output and errors (if any)
        print("Output:", result.stdout)
        print("Errors:", result.stderr)
        
        # Check if the command was successful
        if result.returncode == 0:
            print("Pytest with coverage ran successfully.")
        else:
            print(f"Pytest failed with return code: {result.returncode}")
    except Exception as e:
        print(f"An error occurred: {e}")



def cal_cov(ID, program, response):
    # Modify ID to ensure it starts with a letter (valid Python module name)
    ID = ID.replace('/', '_')

    # Create the filename for the test file
    test_filename = f"cov_test.py"
    module_filename = f"cov.py"
    report_filename = f"Coverage/{ID}_report.json"

    # Write the program (module) and response (test cases) to the respective files
    with open(module_filename, 'w') as f:
        f.write(program)
    
    # Add the import statement to the response to ensure the function is imported
    response_with_import = f"from cov import *\n\n" + response
    
    with open(test_filename, 'w') as f:
        f.write(response_with_import)

    # Run the pytest command
    try:
        run_pytest_with_coverage(ID)
    except subprocess.CalledProcessError as e:
        print(f"Error running pytest: {e}")
        return None

    # Read the generated JSON report
    try:
        print(report_filename)
        with open(report_filename, 'r') as report_file:
            coverage_data = json.load(report_file)
            # Extract the total coverage percentage
            total_coverage = coverage_data['totals']['percent_covered']
            print(f"Code coverage: {total_coverage}%")
    except FileNotFoundError:
        print("Coverage report not found.")
        return None
    except KeyError:
        print("Error reading coverage data.")
        return None

    # Clean up: Remove the generated .py files after running pytest
    try:
        os.remove(module_filename)
        os.remove(test_filename)
        print(f"Removed {module_filename} and {test_filename}")
    except OSError as e:
        print(f"Error removing files: {e}")
    

    
    return total_coverage


if __name__ == "__main__":
#{"task_id": "HumanEval/132", "prompt": "\ndef is_nested(string):\n    '''\n    Create a function that takes a string as input which contains only square brackets.\n    The function should return True if and only if there is a valid subsequence of brackets \n    where at least one bracket in the subsequence is nested.\n\n    is_nested('[[]]') ➞ True\n    is_nested('[]]]]]]][[[[[]') ➞ False\n    is_nested('[][]') ➞ False\n    is_nested('[]') ➞ False\n    is_nested('[[][]]') ➞ True\n    is_nested('[[]][[') ➞ True\n    '''\n", "canonical_solution": "    opening_bracket_index = []\n    closing_bracket_index = []\n    for i in range(len(string)):\n        if string[i] == '[':\n            opening_bracket_index.append(i)\n        else:\n            closing_bracket_index.append(i)\n    closing_bracket_index.reverse()\n    cnt = 0\n    i = 0\n    l = len(closing_bracket_index)\n    for idx in opening_bracket_index:\n        if i < l and idx < closing_bracket_index[i]:\n            cnt += 1\n            i += 1\n    return cnt >= 2\n\n    \n", "test": "def check(candidate):\n\n    # Check some simple cases\n    assert candidate('[[]]') == True, \"This prints if this assert fails 1 (good for debugging!)\"\n    assert candidate('[]]]]]]][[[[[]') == False\n    assert candidate('[][]') == False\n    assert candidate(('[]')) == False\n    assert candidate('[[[[]]]]') == True\n    assert candidate('[]]]]]]]]]]') == False\n    assert candidate('[][][[]]') == True\n    assert candidate('[[]') == False\n    assert candidate('[]]') == False\n    assert candidate('[[]][[') == True\n    assert candidate('[[][]]') == True\n\n    # Check some edge cases that are easy to work out by hand.\n    assert candidate('') == False, \"This prints if this assert fails 2 (also good for debugging!)\"\n    assert candidate('[[[[[[[[') == False\n    assert candidate(']]]]]]]]') == False\n\n", "entry_point": "is_nested"}
    ID = "HumanEval/132"
    program = "def is_nested(string):\n    '''\n    Create a function that takes a string as input which contains only square brackets.\n    The function should return True if and only if there is a valid subsequence of brackets \n    where at least one bracket in the subsequence is nested.\n\n    is_nested('[[]]') ➞ True\n    is_nested('[]]]]]]][[[[[]') ➞ False\n    is_nested('[][]') ➞ False\n    is_nested('[]') ➞ False\n    is_nested('[[][]]') ➞ True\n    is_nested('[[]][[') ➞ True\n    '''\n    opening_bracket_index = []\n    closing_bracket_index = []\n    for i in range(len(string)):\n        if string[i] == '[':\n            opening_bracket_index.append(i)\n        else:\n            closing_bracket_index.append(i)\n    closing_bracket_index.reverse()\n    cnt = 0\n    i = 0\n    l = len(closing_bracket_index)\n    for idx in opening_bracket_index:\n        if i < l and idx < closing_bracket_index[i]:\n            cnt += 1\n            i += 1\n    return cnt >= 2\n"
    response = "import pytest\n\ndef test_no_brackets():\n    assert is_nested(\"no brackets here\") == False\n\ndef test_single_pair():\n    assert is_nested(\"[]\") == False\n\ndef test_two_pairs_nested():\n    assert is_nested(\"[[]]\") == True\n\ndef test_two_pairs_not_nested():\n    assert is_nested(\"[][]\") == False\n\ndef test_multiple_pairs_nested():\n    assert is_nested(\"[[[]]]\") == True\n\ndef test_multiple_pairs_not_nested():\n    assert is_nested(\"[][][]\") == False\n\ndef test_mixed_nested_and_not_nested():\n    assert is_nested(\"[[]][]\") == True\n\ndef test_unbalanced_brackets():\n    assert is_nested(\"[[[]]\") == False\n\ndef test_empty_string():\n    assert is_nested(\"\") == False\n\ndef test_nested_with_other_characters():\n    assert is_nested(\"[a[b]c]\") == True\n\ndef test_not_nested_with_other_characters():\n    assert is_nested(\"[a][b]c\") == False\n"
    cov = cal_cov(ID, program, response)
    print(cov)
    
# pytest --cov=Human_132 --cov-report json:Coverage/132_report.json Human_132_test.py
