"""Convert CSV to JSON"""
import csv
import json
import sys

def csv_to_json(csv_path: str, json_path: str, pretty: bool = True):
    data = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    indent = 2 if pretty else None
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=indent)
    print(f"Converted {len(data)} rows to {json_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: csv_to_json.py <input.csv> <output.json>")
        sys.exit(1)
    csv_to_json(sys.argv[1], sys.argv[2])
