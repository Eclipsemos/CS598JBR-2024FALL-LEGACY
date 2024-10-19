    ###################################################################
    # This is a list of all commands you need to run for MP2 on Colab.
    ###################################################################

    # TODO: Clone your GitHub repository
    %cd /content/
    ! rm -rf ./CS598JBR-Team-9
    ! git clone https://Eclipsemos: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@github.com/Eclipsemos/CS598JBR-Team-9.git
    %cd CS598JBR-Team-9

    # TODO: Replace the file path of selected_humaneval_[seed].jsonl generated in MP1
    input_dataset = "selected_humaneval_171768020378419351865442221048553552766.jsonl"# selected_humaneval_[seed].jsonl

    # Set up requirements for model prompting
    ! bash -x MP2/setup_models.sh
    %cd MP2/
    # TODO: add your seed generated in MP1
    seed = "171768020378419351865442221048553552766"
    task_1_vanilla_json = "task_1_" + seed + "_vanilla.jsonl"
    task_1_vanilla_prompt_json = "task_1_" + seed + "_vanilla_prompt.jsonl"
    # Generate vanilla prompt
    ! python3 script.py input_dataset task_1_vanilla_prompt_json
    #task_1_crafted_json = "task_1_" + seed + "_crafted.jsonl"
    #task_2_vanilla_json = "task_2_" + seed + "_vanilla.jsonl"
    #task_2_crafted_json = "task_2_" + seed + "_crafted.jsonl"
    
    
    # Prompt the models, you can create your `MP2/task_1.py, MP2/task_2.py, MP2/task_3.py` by modifying `MP2/task_[ID].py`
    # The {input_dataset} is the JSON file consisting of 20 unique programs for your group that you generated in MP1 (selected_humaneval_[seed].jsonl)
    ! python3 task_1.py {task_1_vanilla_prompt_json} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_1_vanilla_json} "True" |& tee task_1_vanilla.log
    #! python3 task_1.py {input_dataset} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_1_crafted_json} "False" |& tee task_1_crafted.log
    #! python3 task_2.py {input_dataset} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_2_vanilla_json} "True" |& tee task_2_vanilla.log
    #! python3 task_2.py {input_dataset} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_2_crafted_json} "False" |& tee task_2_crafted.log

    # Old commands
    #! python3 task_1.py {task_1_json} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_1_json} "True" |& tee task_1_prompt.log
    #! python3 MP2/task_2.py {input_dataset} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_2_json} "True" |& tee task_2_prompt.log
    #! python3 MP2/task_3.py {input_dataset} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_3_json} "True" |& tee task_3_prompt.log
    #! evaluate_functional_correctness {task_3_json} |& tee task_3_evaluate.log

    #%cd ..

    # git push all nessacery files (e.g., *jsonl, *log) to your GitHub repository