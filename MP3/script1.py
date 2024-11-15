import jsonlines

def van_generate_prompt(entry, declaration):
    problem = entry["prompt"]
    solution = entry["canonical_solution"]
    prompt = f"""You are an AI programming assistant utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.
### Instruction:
Can you translate the following Python code into Java?
The output Java code must be enclosed between [Java Start] and [Java End], not markdown style.
The final result should be  enclosed between [Java Start] and [Java End], not markdown style.
The output Java code should align with declaration code and it's import module: {declaration}. 

Here is Python code:
{problem}
{solution}

### Response:
"""
    return prompt

def craft_generate_prompt(entry, declaration):
    problem = entry["prompt"]
    solution = entry["canonical_solution"]
    prompt = f"""You are an AI programming assistant utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.
### Instruction:
Can you translate the following Python code into Java?
The new Java code must be enclosed between [Java Start] and [Java End], not ```java```!

{problem}
{solution}

### Response:

"""
    return prompt


if __name__ == "__main__":
    dataset = []
    filepath = "selected_humanevalx_python_171768020378419351865442221048553552766.jsonl"
    with jsonlines.open(filepath) as reader:
        for line in reader: 
            dataset.append(line)
    for entry in dataset:
        prompt1 = van_generate_prompt(entry)
        prompt2 = craft_generate_prompt(entry)
        print(prompt1)
        print(prompt2)