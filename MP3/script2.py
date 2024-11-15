import jsonlines

def van_generate_prompt(entry):
    problem = entry["prompt"]
    solution = entry["buggy_solution"]
    declaration = entry["declaration"]
    prompt = f"""You are an AI programming assistant. 
    You are an AI programming assistant utilizing the DeepSeek Coder model, developed by DeepSeek Company, 
    and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, 
    and other non-computer science questions, you will refuse to answer.
### Instruction:

{declaration}
{solution}

Is the above code buggy or correct? Please explain your step by step reasoning. The prediction should be enclosed within <start> and <end> tags. For example: <start>Buggy<end>
#### NOTICE: The prediction should be enclosed within <start> and <end> tags ONLY, and the predciont should be either "Correct" or "Incorrect" ####
### Response:

"""
    return prompt

def craft_generate_prompt(entry):
    problem = entry["prompt"]
    solution = entry["buggy_solution"]
    declaration = entry["declaration"]
    prompt = f"""You are an AI programming assistant. You are an AI programming assistant utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.
### Instruction:

{declaration}
{solution}

Is the above code buggy or correct? Please explain your step by step reasoning. 
The prediction should be enclosed within <start> and <end> tags. For example: <start>Buggy<end>
Think through the translation process step-by-step, try to execute the code and fine the possible error.
And provide a detailed, step-by-step explanation of your reasoning process to justify your determination.
- If the code is buggy, identify the specific issues, explain why they occur, and suggest a fix.
- If the code is correct, confirm its correctness and explain how it works.

#### NOTICE: The prediction should be enclosed within <start> and <end> tags ONLY, and the predciont should be either "Correct" or "Incorrect" ####

### Response:

"""
    return prompt


if __name__ == "__main__":
    dataset = []
    filepath = "selected_humanevalpack_171768020378419351865442221048553552766.jsonl"
    with jsonlines.open(filepath) as reader:
        for line in reader: 
            dataset.append(line)
    for entry in dataset:
        prompt1 = van_generate_prompt(entry)
        prompt2 = craft_generate_prompt(entry)
        print(prompt1)
        print(prompt2)
