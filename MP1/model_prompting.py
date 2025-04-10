    import jsonlines
    import sys
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

    #####################################################
    # Please finish all TODOs in this file for MP1;
    # do not change other code/formatting.
    #####################################################

    def save_file(content, file_path):
        with open(file_path, 'w') as file:
            file.write(content)


    # def prompt_model(problem):
    #   tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-6.7b-instruct", trust_remote_code=True)
    #   # model = AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-coder-6.7b-base", trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()
    #   model = AutoModelForCausalLM.from_pretrained(
    #           pretrained_model_name_or_path='deepseek-ai/deepseek-coder-6.7b-instruct',
    #           device_map='auto',
    #           torch_dtype=torch.bfloat16,
    #           # temperature = 0,
    #           # do_sample=False,
    #           quantization_config=BitsAndBytesConfig(
    #               load_in_4bit=True,
    #               bnb_4bit_compute_dtype=torch.bfloat16,
    #               bnb_4bit_use_double_quant=True,
    #               bnb_4bit_quant_type='nf4'
    #           ),
    #       )

    def prompt_model(dataset, model_name = "deepseek-ai/deepseek-coder-6.7b-base", quantization = True):
        print(f"Working with {model_name} quantization {quantization}...")
        
        # TODO: download the model
        
    
        if quantization:
            # TODO: load the model with quantization
            # bnb_config = BitsAndBytesConfig(load_in_8bit=True)
            # model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config)
            tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            # model = AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-coder-6.7b-base", trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()
            model = AutoModelForCausalLM.from_pretrained(
                    pretrained_model_name_or_path= model_name,
                    device_map='auto',
                    torch_dtype=torch.bfloat16,
                    # temperature = 0,
                    # do_sample=False,
                    quantization_config=BitsAndBytesConfig(
                        load_in_4bit=True,
                        bnb_4bit_compute_dtype=torch.bfloat16,
                        bnb_4bit_use_double_quant=True,
                        bnb_4bit_quant_type='nf4'
                    ),
                )


            
        else:
            # TODO: load the model without quantization
            model = AutoModelForCausalLM.from_pretrained(model_name)
            

        results = []
        for case in dataset:
            prompt = case['prompt']
            # TODO: prompt the model and get the response
            # tokenizer = AutoTokenizer.from_pretrained(model_name)
            # inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
            # outputs = model.generate(**inputs, max_length=512, num_return_sequences=1, num_beams=1, no_repeat_ngram_size=2, early_stopping=True)
            # response = tokenizer.decode(outputs[0], skip_special_tokens=True)

            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            outputs = model.generate(**inputs,
                                    max_length=1024,
                                    temperature = 0,
                                    do_sample=False,)
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)

            print(f"Task_ID {case['task_id']}:\nPrompt:\n{prompt}\nResponse:\n{response}")
            results.append(dict(task_id=case["task_id"], completion=response))
        return results

    def read_jsonl(file_path):
        dataset = []
        with jsonlines.open(file_path) as reader:
            for line in reader: 
                dataset.append(line)
        return dataset

    def write_jsonl(results, file_path):
        with jsonlines.open(file_path, "w") as f:
            for item in results:
                f.write_all([item])

    if __name__ == "__main__":
        """
        This Python script is to run prompt LLMs for code synthesis.
        Usage:
        `python3 model_prompting.py <input_dataset> <model> <output_file> <if_quantization>`|& tee prompt.log

        Inputs:
        - <input_dataset>: A `.jsonl` file, which should be your team's dataset containing 20 HumanEval problems.
        - <model>: Specify the model to use. Options are "deepseek-ai/deepseek-coder-6.7b-base" or "deepseek-ai/deepseek-coder-6.7b-instruct".
        - <output_file>: A `.jsonl` file where the results will be saved.
        - <if_quantization>: Set to 'True' or 'False' to enable or disable model quantization.
        
        Outputs:
        - You can check <output_file> for detailed information.
        """
        args = sys.argv[1:]
        input_dataset = args[0]
        model = args[1]
        output_file = args[2]
        if_quantization = args[3] # True or False
        
        if not input_dataset.endswith(".jsonl"):
            raise ValueError(f"{input_dataset} should be a `.jsonl` file!")
        
        if not output_file.endswith(".jsonl"):
            raise ValueError(f"{output_file} should be a `.jsonl` file!")
        
        quantization = True if if_quantization == "True" else False
        
        dataset = read_jsonl(input_dataset)
        results = prompt_model(dataset, model, quantization)
        write_jsonl(results, output_file)
