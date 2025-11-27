import pandas as pd
import json
import os

def save_to_csv(data, filename):
    """Saves a list of dictionaries to a CSV file."""
    if not data:
        print("No data to save.")
        return
    
    df = pd.DataFrame(data)
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def save_to_json(data, filename):
    """Saves data to a JSON file."""
    if not data:
        print("No data to save.")
        return

    # Ensure directory exists
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")
