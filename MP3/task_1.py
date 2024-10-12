import jsonlines
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

#####################################################
# Please finish all TODOs in this file for MP3/task1;
#####################################################

def save_file(content, file_path):
    with open(file_path, 'w') as file:
        file.write(content)

def prompt_model(dataset, model_name = 'deepseek-ai/deepseek-coder-6.7b-instruct'):
    print(f'Working with {model_name}...')
    
    # TODO: download the model
    # TODO: load the model with quantization

    results = []
    for entry in dataset:
        
        # TODO: generate prompt based on code and test input/output.
        prompt = ''
        
        # TODO: prompt the model and get the response
        model_response = ''
    
        print(f"Entry_ID {entry['id']}:\nPrompt:\n{prompt}\nResponse:\n{model_response}")
        
        entry_result = {
            'id': entry['id'], 
            'prompt': prompt, 
            'model_response': model_response, 
            'test_input': entry['test_IO'][0]['input'], 
            'expected_test_output': entry['test_IO'][0]['output']
        }
        results.append(entry_result)
    return results

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

if __name__ == '__main__':
    '''
    This Python script is to run prompt LLMs for code synthesis.
    Usage:
    `python3 task1.py <input_dataset> <output_file> `|& tee task_1.log

    Inputs:
    - <input_dataset>: A `.jsonl` file, which should be your team's dataset containing 20 HumanEval problems.
    - <output_file>: A `.jsonl` file where the results will be saved.
    
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
    results = prompt_model(dataset)
    write_jsonl(results, output_file)