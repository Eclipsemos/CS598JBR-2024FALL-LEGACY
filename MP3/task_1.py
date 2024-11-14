import jsonlines
import sys
import re
import subprocess
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from script1 import van_generate_prompt, craft_generate_prompt  # assuming these functions are in script1

#####################################################
# Please finish all TODOs in this file for MP3/task_1
#####################################################

def save_file(content, file_path):
    with open(file_path, 'w') as file:
        file.write(content)

def extract_java_code(response):
    """Extract Java code between [Java Start] and [Java End]"""
    match = re.search(r'\[Java Start\](.*?)\[Java End\]', response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def run_java_code(java_code, test_code):
    """Save Java code to a file, compile it, and run it with provided tests.
    Returns True if tests pass, False if compilation or execution fails."""
    # Ensure imports are correctly placed at the top
    imports = "import java.util.*;\n\n"
    
    # Create the Solution class wrapping the extracted Java code
    solution_code = "public class Solution {\n" + java_code + "\n}\n"
    
    # Combine imports, Solution, and Main classes into a single file
    combined_code = imports + solution_code + "\n" + test_code.replace("public class Main", "public class Main")

    with open("TempTest.java", "w") as f:
        f.write(combined_code)

    try:
        # Compile the Java code
        subprocess.check_output(["javac", "TempTest.java"], stderr=subprocess.STDOUT)
        
        # Run the compiled Java code
        result = subprocess.run(["java", "Main"], capture_output=True, text=True)
        
        # Check if the test output contains "All tests passed" to confirm success
        return "All tests passed" in result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Compilation or execution error: {e.output.decode()}")
        # Return False to indicate the test did not pass due to an error
        return False



def read_jsonl(file_path):
    """Read .jsonl file and return the dataset"""
    dataset = []
    with jsonlines.open(file_path) as reader:
        for line in reader: 
            dataset.append(line)
    return dataset

def write_jsonl(results, file_path):
    """Write results to a .jsonl file"""
    with jsonlines.open(file_path, "w") as f:
        for item in results:
            f.write(item)

def load_datasets(python_dataset_path, java_dataset_path):
    """Load both Python and Java datasets, mapping task_id to Java test cases"""
    python_dataset = read_jsonl(python_dataset_path)
    java_dataset = read_jsonl(java_dataset_path)
    
    # Map each task_id in the Java dataset to its test code
    java_tests = {entry['task_id']: entry['test'] for entry in java_dataset}
    
    return python_dataset, java_tests

def prompt_model(python_dataset, java_tests, model_name="deepseek-ai/deepseek-coder-6.7b-instruct", vanilla=True):
    """Prompt the model with Python dataset and evaluate responses with Java tests"""
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path= model_name,
            device_map='auto',
            torch_dtype=torch.bfloat16,
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type='nf4'
            ),
        )
    
    results = []
    for entry in python_dataset:
        # Generate prompt and model response
        prompt = van_generate_prompt(entry) if vanilla else craft_generate_prompt(entry)
        
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_length=1024, temperature=0, do_sample=False)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract Java code
        java_code = extract_java_code(response)
        
        # Retrieve the corresponding Java test case
        task_id = entry['task_id']
        java_test_code = java_tests.get(task_id, "").replace("python", "java")
        
        # Run the Java code with the test cases and determine if it passed
        if java_code and java_test_code:
            is_correct = run_java_code(java_code, java_test_code)
        else:
            is_correct = False

        # Append results
        results.append({
            "task_id": task_id,
            "prompt": prompt,
            "response": response,
            "is_correct": is_correct
        })
    
    return results

if __name__ == "__main__":
    """
    This Python script is to run prompt LLMs for code translation.
    Usage:
    `python3 task_1.py <input_python_dataset> <model> <output_file> <if_vanilla>`|& tee prompt.log

    Inputs:
    - <input_python_dataset>: A `.jsonl` file, which should be your team's dataset containing 20 HumanEval problems.
    - <model>: Specify the model to use. Options are "deepseek-ai/deepseek-coder-6.7b-base" or "deepseek-ai/deepseek-coder-6.7b-instruct".
    - <output_file>: A `.jsonl` file where the results will be saved.
    - <if_vanilla>: Set to 'True' or 'False' to enable vanilla prompt
    
    Outputs:
    - You can check <output_file> for detailed information.
    """
    args = sys.argv[1:]
    input_python_dataset = args[0]
    model = args[1]
    output_file = args[2]
    if_vanilla = args[3]  # True or False

    if not input_python_dataset.endswith(".jsonl"):
        raise ValueError(f"{input_python_dataset} should be a `.jsonl` file!")

    if not output_file.endswith(".jsonl"):
        raise ValueError(f"{output_file} should be a `.jsonl` file!")

    vanilla = True if if_vanilla == "True" else False

    # Load both Python and Java datasets
    input_java_dataset = input_python_dataset.replace("python", "java")
    python_dataset, java_tests = load_datasets(input_python_dataset, input_java_dataset)

    # Generate results using the Java test cases for verification
    results = prompt_model(python_dataset, java_tests, model, vanilla)
    write_jsonl(results, output_file)
