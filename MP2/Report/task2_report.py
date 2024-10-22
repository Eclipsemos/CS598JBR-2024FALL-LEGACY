import os
import json
import re
import pandas as pd

def analyze_pytest_output(file_path):
    # Dictionary to store the analysis of each task
    analysis_results = {}

    # Regex to capture the number of passed or failed tests
    test_result_pattern = re.compile(r"(\d+ failed, \d+ passed|\d+ passed|\d+ failed)")
    # Regex to capture the Task_ID like HumanEval/10
    task_id_pattern = re.compile(r"Task ID: (\w+_\d+_\w+_)")

    task_id = None
    test_result = None

    # Open the file and process each line
    with open(file_path, 'r') as file:
        lines = file.readlines()


    # Process each line
    for line in lines:
        # Search for Task_ID
        task_id_match = task_id_pattern.search(line)
        if task_id_match:
            print(task_id_match)
            task_id = task_id_match.group(1)

        # Search for the test result (e.g., 2 passed or 1 failed, 4 passed)
        test_result_match = test_result_pattern.search(line)
        if test_result_match:
            test_result = test_result_match.group(0)

        # If both task_id and test_result are found, save them and reset for the next case
        if task_id and test_result:
            analysis_results[task_id] = test_result
            task_id = None
            test_result = None

    return analysis_results


def generate_table(results):
    data = []
    
    # Process the results and create entries for vanilla and crafted
    processed_tasks = set()

    for task_id, result in results.items():
        base_task_id = task_id.rsplit('_', 2)[0]  # Extract the task ID without "vanilla" or "crafted"
        if base_task_id in processed_tasks:
            continue
        
        vanilla_key = f"{base_task_id}_vanilla_"
        crafted_key = f"{base_task_id}_crafted_"

        # Extract results for vanilla and crafted cases
        vanilla_result = results.get(vanilla_key, "N/A")
        crafted_result = results.get(crafted_key, "N/A")
        
        # Calculate pass rates for both vanilla and crafted cases
        vanilla_passes, vanilla_total = extract_pass_fail(vanilla_result)
        crafted_passes, crafted_total = extract_pass_fail(crafted_result)

        # Add data row with task ID, results and pass percentages
        data.append({
            "test case": base_task_id,
            "vanilla (passed/total)": f"{vanilla_passes}/{vanilla_total}",
            "vanilla pass%": f"{(vanilla_passes/vanilla_total)*100:.2f}%" if vanilla_total > 0 else "N/A",
            "crafted (passed/total)": f"{crafted_passes}/{crafted_total}",
            "crafted pass%": f"{(crafted_passes/crafted_total)*100:.2f}%" if crafted_total > 0 else "N/A"
        })
        
        processed_tasks.add(base_task_id)

    # Convert to pandas DataFrame
    df = pd.DataFrame(data)
    return df

def extract_pass_fail(result_str):
    # This function extracts number of passed and total tests from result string
    match = re.match(r"(\d+) failed, (\d+) passed", result_str)
    if match:
        failed = int(match.group(1))
        passed = int(match.group(2))
        return passed, passed + failed
    else:
        match_passed = re.match(r"(\d+) passed", result_str)
        if match_passed:
            passed = int(match_passed.group(1))
            return passed, passed
        else:
            match_failed = re.match(r"(\d+) failed", result_str)
            if match_failed:
                failed = int(match_failed.group(1))
                return 0, failed
    return 0, 0


def parse_json(file_path):
    """Parse a JSON file and return the percent_covered."""
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data.get("totals", {}).get("percent_covered", 0)

def generate_report(directory):
    """Generate a report based on crafted and vanilla reports in the given directory."""
    report = []
    total_craft_covered = 0
    total_vanilla_covered = 0
    count = 0

    # Dictionary to temporarily hold coverage data for each id
    coverage_data = {}

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            # Extract ID and report type from the filename
            parts = filename.split("_")
            if len(parts) >= 3:
                eval_id = parts[1]
                report_type = parts[2]

                # Parse the coverage data
                coverage = parse_json(os.path.join(directory, filename))

                # Store the coverage in the temporary dictionary
                if eval_id not in coverage_data:
                    coverage_data[eval_id] = {"crafted": None, "vanilla": None}
                
                if report_type == "crafted":
                    coverage_data[eval_id]["crafted"] = coverage
                elif report_type == "vanilla":
                    coverage_data[eval_id]["vanilla"] = coverage

    # Generate the final report
    for eval_id, data in coverage_data.items():
        if data["crafted"] is not None and data["vanilla"] is not None:
            craft_coverage = data["crafted"]
            vanilla_coverage = data["vanilla"]
            report.append({
                "id": eval_id,
                "crafted_percent_covered": craft_coverage,
                "vanilla_percent_covered": vanilla_coverage
            })
            total_craft_covered += craft_coverage
            total_vanilla_covered += vanilla_coverage
            count += 1

    # Calculate overall coverage
    overall_craft_covered = total_craft_covered / count if count else 0
    overall_vanilla_covered = total_vanilla_covered / count if count else 0

    # Print the general report with details for each case
    print("General Report")
    print("====================")
    for case in report:
        print(f"ID: {case['id']}")
        print(f"  Crafted Coverage: {case['crafted_percent_covered']}%")
        print(f"  Vanilla Coverage: {case['vanilla_percent_covered']}%")
        print("--------------------")

    # Print the overall report
    print("Overall Report")
    print("====================")
    print(f"Average Crafted Coverage: {overall_craft_covered}%")
    print(f"Average Vanilla Coverage: {overall_vanilla_covered}%")

if __name__ == "__main__":
    # Specify the directory where the JSON files are located
    coverage_directory = "../Coverage"
    
    # Generate the report
    generate_report(coverage_directory)


    # Analyze the file
    results = analyze_pytest_output('cases.txt')
    # print(len(results.items()))
    # Print the results
    # for task_id, result in results.items():
    #     print(f"Task_ID: {task_id}, Result: {result}")
    
    df = generate_table(results)

    print(df)
