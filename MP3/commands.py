###################################################################
# This is a list of all commands you need to run for MP3 on Colab.
###################################################################

# TODO: Update Your NetIDs in alphabetical order
NetIDs = ["sampleID1", "sampleID2", "sampleID3", "sampleID4"]
NetIDs_str = " ".join(NetIDs)

# TODO: Clone your GitHub repository
! git clone [Your GitHub Link]
%cd [Your GitHub Repo]/MP3

# Set up requirements for dataset generation
! bash -x setup_dataset.sh

# dataset generation
! python3 codenet_dataset_generation.py {NetIDs_str} |& tee codenet_dataset_generation.log

seed = "<your_seed>"
# TODO: Replace the file path of selected_codenet_[seed].jsonl generated in previous step
input_dataset = "selected_codenet_" + seed + ".jsonl"

# Set up requirements for model prompting
! bash -x setup_models.sh

task_1_response = "task_1_response_" + seed + ".jsonl"
task_1_evaluation = "task_1_evaluation_" + seed + ".jsonl"

# Task 1
! python3 task_1.py {input_dataset} {task_1_response} "True" |& tee task_1.log
! python3 evaluation_translation.py {task_1_response} {task_1_evaluation} |& tee task_1_evaluation.log

# Task 2

# TODO: Replace the file path of selected_humaneval_[seed].jsonl generated in MP1
humaneval_input_dataset = "selected_humaneval_" + seed + ".jsonl"

# Prompt the models, you can modify `MP3/task_2.py`
# The {input_dataset} is the JSON file consisting of 20 unique programs for your group that you generated in MP1 (selected_humaneval_[seed].jsonl)
! python3 task_2_dataset_generation.py {humaneval_input_dataset}

task_2_vanilla_json = "task_2_" + seed + "_vanilla.jsonl"
task_2_crafted_json = "task_2_" + seed + "_crafted.jsonl"
humanevalpack_input_dataset = "selected_humanevalpack_" + seed + ".jsonl"

! python3 task_2.py {input_dataset} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_2_vanilla_json} "True" |& tee task_2_vanilla.log
! python3 task_2.py {input_dataset} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_2_crafted_json} "False" |& tee task_2_crafted.log

%cd ..

# git push all nessacery files (e.g., *jsonl, *log) to your GitHub repository
