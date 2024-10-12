import sys
import random
import hashlib
import json
import jsonlines

################################################
# Please do not change this file when doing MP3.
################################################

def generate_seed(netIDs):
    seed = int(hashlib.md5('_'.join(netIDs).encode()).hexdigest(), 16)
    return seed

def select_random_problems(netIDs, num_problems=20, original_dataset="codenet.json"):
    seed = generate_seed(netIDs)
    random.seed(seed)
    print(f"NetIDs {netIDs} with seed {seed}")

    python_codenet = []
    with open(original_dataset, 'r') as file:
        item_list = json.load(file)
        python_codenet = [item for item in item_list if item["language"] == "Python"]

    selected_problems = random.sample(python_codenet, num_problems)
    selected_problems_output = f"selected_codenet_{seed}.jsonl"
    with jsonlines.open(selected_problems_output, "w") as f:
        for item in selected_problems:
            f.write_all([item])
    print(f"Selected {num_problems} problems saved to {selected_problems_output}")

if __name__ == "__main__":
    args = sys.argv[1:]
    select_random_problems(args)

