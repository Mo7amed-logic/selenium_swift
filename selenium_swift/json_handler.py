import json
import os

def load_json_data(json_file_path: str) -> dict:
    """Load data from a JSON file and return it as a dictionary."""
    if not os.path.exists(json_file_path):
        print(f"File not found: {json_file_path}")
        return None
    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading the file: {e}")
        return None

def save_json_data(data: dict, json_file_path: str) -> bool:
    """Save a dictionary as a JSON file."""
    try:
        with open(json_file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data saved successfully to {json_file_path}")
        return True
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
        return False

def pretty_print_json(data: dict):
    """Print JSON data in a human-readable format."""
    print(json.dumps(data, indent=4))
