import os
import json

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
    coverage_directory = "Coverage"
    
    # Generate the report
    generate_report(coverage_directory)
