import jsonlines
import os
import re
import subprocess
from subprocess import Popen, PIPE
import sys

def read_jsonl(file_path):
    dataset = []
    with jsonlines.open(file_path) as reader:
        for line in reader: 
            dataset.append(line)
    return dataset


def write_jsonl(results, file_path):
    with jsonlines.open(file_path, 'w') as f:
        for item in results:
            f.write_all([item])

#TODO: Feel free to adjust/improve function `parse_response`.
def parse_response(entry_id, content):
    response = content.split("### Response:")[-1]
    code = re.search(r'```java(.*?)```', response, re.DOTALL)
    java_code = code.group(1).strip()
    java_code = re.sub(r'(public\s*class\s*\w+\s*\{)', 'public class ' + entry_id + ' {', java_code)
    print(f"Parsing Java Code:\n{java_code}\n")
    return java_code

def write_file(file_path, content):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    except:
        pass
    f = open(file_path, "w")
    f.write(content)
    f.close()


def run_java_code(entry_id, java_code, test_input, expected_test_output):
    java_file_path = f"{entry_id}.java"
    write_file(java_file_path, java_code)
    try:
        subprocess.run(f"javac {java_file_path}", check=True, capture_output=True, shell=True, timeout=30)
        p = Popen(['java', java_file_path.split(".")[0]], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        try:
            stdout, stderr_data = p.communicate(input=test_input.encode(), timeout=10)
        except subprocess.TimeoutExpired:
            return "Runtime Error"
        
        actual_output = stdout.decode().strip()
        print(f"Actual Output: {actual_output}")
        print(f"Expected Output: {expected_test_output.strip()}")
        if actual_output == expected_test_output:
            return "Test Pass"
        else:
            if stderr_data.decode()=='':
                return "Test Failure"
            else:
                return "Runtime Error"
    except:
        return "CompilationError"
            
def evaluate_translation(dataset):
    results = []
    for entry in dataset:
        entry_id = entry["id"]
        model_response = entry["model_response"]
        test_input = entry["test_input"]
        expected_test_output = entry["expected_test_output"]
        
        print(f"Working on {entry_id}")
        java_code = parse_response(entry_id, model_response)
        test_result = run_java_code(entry_id, java_code, test_input, expected_test_output)
        print(f"ID: {entry_id} Result: {test_result}")
        entry_result = {
            "id": entry_id,
            "model_response": model_response,
            "java_code": java_code,
            "test_result": test_result,
        }
        results.append(entry_result)
        
    return results

if __name__ == '__main__':
    '''
    This Python script is to evaluate code translation.
    Usage:
    `python3 evaluation_translation.py <input_dataset> <output_file> `|& tee evaluation_translation.log

    Inputs:
    - <input_dataset>: A `.jsonl` file, which should be the results from MP3/task1
    - <output_file>: A `.jsonl` file where the results will be saved at.
    
    Outputs:
    - You can check <output_file> for detailed information.
    '''
    args = sys.argv[1:]
    input_dataset = args[0]
    output_file = args[1]
    
    if not input_dataset.endswith('.jsonl'):
        raise ValueError(f'{input_dataset} should be a `.jsonl` file!')
    
    if not output_file.endswith('.jsonl'):
        raise ValueError(f'{output_file} should be a `.jsonl` file!')
    
    dataset = read_jsonl(input_dataset)
    results = evaluate_translation(dataset)
    write_jsonl(results, output_file)