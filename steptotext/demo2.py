import re
import pandas as pd
from typing import List, Dict

def parse_step_file(file_path: str) -> List[Dict[str, str]]:
    """
    Parses a STEP file and extracts entities, their types, and attributes.
    """
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Regex to match entity lines (e.g., #10=PROPERTY_DEFINITION_REPRESENTATION(#14,#12))
    entity_pattern = re.compile(r'#(\d+)=([A-Z_]+)\((.*)\);')

    for line in lines:
        match = entity_pattern.match(line.strip())
        if match:
            entity_id = match.group(1)
            entity_type = match.group(2)
            attributes = match.group(3)
            data.append({
                'Entity ID': entity_id,
                'Entity Type': entity_type,
                'Attributes': attributes
            })

    return data

def save_to_csv(data: List[Dict[str, str]], output_file: str) -> None:
    """
    Saves the extracted data to a CSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)

def step_to_csv(input_file: str, output_file: str) -> None:
    """
    Converts a STEP file to a structured CSV file.
    """
    data = parse_step_file(input_file)
    save_to_csv(data, output_file)

# Example usage
if __name__ == "__main__":
    input_step_file = "/home/anaxturia/Anax_practice/steptotext/dataset/CORE HOUSING_IT0588-01.stp"  # Replace with your STEP file path
    output_csv_file = "stp_output.csv"   # Replace with your desired CSV file path
    step_to_csv(input_step_file, output_csv_file)