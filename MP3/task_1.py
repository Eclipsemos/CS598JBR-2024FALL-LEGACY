import jsonlines
import sys
import re
import subprocess
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from script1 import van_generate_prompt, craft_generate_prompt  # assuming these functions are in script1

def extract_java_code(response):
    """Extract Java code between the last [Java Start] and [Java End]"""
    matches = re.findall(r'\[Java Start\](.*?)\[Java End\]', response, re.DOTALL)
    if matches:
        # Get the last match, which should be the actual Java code
        return matches[-1].strip()
    return None

def run_java_code(java_code, test_code):
    """Combine declaration, Java code, and test code, compile, and run tests.
    Returns True if tests pass; False if compilation or execution fails."""
    
    # Combine declaration, Java solution, and test code
    combined_code = java_code + "\n\n" + test_code

    # Write to Main.java
    with open("Main.java", "w") as f:
        f.write(combined_code)
        #print("declaration:"+ declaration)
        print("java_code:"+ java_code)
        print("test_code:"+ test_code)

    try:
        # Compile Main.java
        subprocess.check_output(["javac", "Main.java"], stderr=subprocess.STDOUT)
        
        # Run the compiled Java code
        result = subprocess.run(["java", "Main"], capture_output=True, text=True)
        
        # Check if all tests passed by evaluating the output
        return "All tests passed" in result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Compilation or execution error: {e.output.decode()}")
        return False

def load_datasets(python_file, java_file):
    # Load Python dataset
    with jsonlines.open(python_file) as reader:
        python_dataset = [entry for entry in reader]
    
    # Load Java dataset
    with jsonlines.open(java_file) as reader:
        java_dataset = [entry for entry in reader]
    
    return python_dataset, java_dataset

def write_jsonl(results, file_path):
    with jsonlines.open(file_path, "w") as writer:
        writer.write_all(results)

def prompt_model(python_dataset, java_dataset, model_name="deepseek-ai/deepseek-coder-6.7b-instruct", vanilla=True):
    print(f"Working with {model_name} prompt type {vanilla}...")
    
    # Initialize tokenizer and model with quantization
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        pretrained_model_name_or_path=model_name,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        quantization_config=BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        ),
    )
    
    results = []
    for py_entry, java_entry in zip(python_dataset, java_dataset):
        # Retrieve declaration and test code from Java dataset entry
        declaration = java_entry.get("declaration", "")
        test_code = java_entry.get("test", "")

        # Generate prompt from Python dataset entry
        prompt = van_generate_prompt(py_entry, declaration) if vanilla else craft_generate_prompt(py_entry, declaration)

        # Generate Java code from model
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_length=1024, temperature=0, do_sample=False)
        raw_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract Java code between [Java Start] and [Java End] tags
        java_code = extract_java_code(raw_response)
        if java_code is None:
            print(f"Failed to extract Java code for task {py_entry['task_id']}")
            is_correct = False
        else:
            # Run the Java code using the declaration and test code
            is_correct = run_java_code(java_code, test_code)

        # print(f"Task_ID {py_entry['task_id']}:\nPrompt:\n{prompt}\nGenerated Java Code:\n{java_code}\nIs Correct:\n{is_correct}")
        
        # Save results for each task
        results.append({
            "task_id": py_entry["task_id"],
            "prompt": prompt,
            "response": java_code,
            "is_correct": is_correct
        })
    
    return results

if __name__ == "__main__":
    """
    This Python script is to run prompt LLMs for code translation.
    Usage:
    `python3 task_1.py <input_python_dataset> <model> <output_file> <if_vanilla>` |& tee prompt.log

    Inputs:
    - <input_python_dataset>: A `.jsonl` file with 20 HumanEval problems.
    - <model>: Model to use, like "deepseek-ai/deepseek-coder-6.7b-instruct".
    - <output_file>: Output `.jsonl` file for results.
    - <if_vanilla>: Set to 'True' or 'False' for vanilla prompt type.
    """
    
    args = sys.argv[1:]
    input_python_dataset = args[0]
    model = args[1]
    output_file = args[2]
    if_vanilla = args[3]  # "True" or "False"

    if not input_python_dataset.endswith(".jsonl"):
        raise ValueError(f"{input_python_dataset} should be a `.jsonl` file!")
    
    if not output_file.endswith(".jsonl"):
        raise ValueError(f"{output_file} should be a `.jsonl` file!")
    
    vanilla = True if if_vanilla == "True" else False

    # Load both Python and Java datasets
    input_java_dataset = input_python_dataset.replace("python", "java")
    python_dataset, java_dataset = load_datasets(input_python_dataset, input_java_dataset)

    # Generate results using the Java test cases for verification
    results = prompt_model(python_dataset, java_dataset, model, vanilla)
    write_jsonl(results, output_file)
