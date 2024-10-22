###################################################################
# This is a list of all commands you need to run for MP2 on Colab.
###################################################################

# Clone GitHub repository
%cd /content/
! rm -rf ./CS598JBR-Team-9
! git clone https://Eclipsemos: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@github.com/Eclipsemos/CS598JBR-Team-9.git
%cd CS598JBR-Team-9

# Dataset generated
input_dataset = "selected_humaneval_171768020378419351865442221048553552766.jsonl"# selected_humaneval_[seed].jsonl

# Set up requirements for model prompting
! bash -x MP2/setup_models.sh
%cd MP2/
# Input & Output files generated
seed = "171768020378419351865442221048553552766"
task_1_vanilla_json = "task_1_" + seed + "_vanilla.jsonl"
task_1_vanilla_prompt_json = "task_1_" + seed + "_vanilla_prompt.jsonl"
task_1_crafted_json = "task_1_" + seed + "_crafted.jsonl"
task_1_crafted_prompt_json = "task_1_" + seed + "_crafted_prompt.jsonl"
# Vanilla prompt generate
! python3 task1_script.py {input_dataset} {task_1_vanilla_prompt_json}
# Crafted prompt generate
! python3 task1_script.py {input_dataset} {task_1_crafted_prompt_json}

# [TASK1] Vanilla
! python3 task_1.py {task_1_vanilla_prompt_json} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_1_vanilla_json} "True" |& tee task_1_vanilla.log
# [TASK1] Crafted
! python3 task_1.py {task_1_crafted_prompt_json} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_1_crafted_json} "False" |& tee task_1_crafted.log

# Input & Output files generated
task_2_vanilla_json = "task_2_" + seed + "_vanilla.jsonl"
task_2_crafted_json = "task_2_" + seed + "_crafted.jsonl"
task_2_prompt_json = "task_2_" + seed + "_prompt.jsonl"
# Vanilla & Crafted prompt generate
! python3 task2_script.py {input_dataset} {task_2_prompt_json}
! python3 task_2.py {task_2_prompt_json} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_2_vanilla_json} "True" |& tee task_2_vanilla.log
! python3 task_2.py {task_2_prompt_json} "deepseek-ai/deepseek-coder-6.7b-instruct" {task_2_crafted_json} "False" |& tee task_2_crafted.log
`
#%cd ..

# git push all nessacery files (e.g., *jsonl, *log) to your GitHub repository