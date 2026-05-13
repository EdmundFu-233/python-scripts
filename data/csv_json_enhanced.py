"""Enhanced CSV to JSON with nested structure support"""
import csv
import json

def csv_to_json(csv_path, json_path, nested=False, delimiter="."):
    data = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if nested:
                obj = {}
                for key, val in row.items():
                    parts = key.split(delimiter)
                    current = obj
                    for part in parts[:-1]:
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                    current[parts[-1]] = val
                data.append(obj)
            else:
                data.append(row)
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Converted {len(data)} rows to {json_path}")

if __name__ == "__main__":
    import sys
    nested = "--nested" in sys.argv
    csv_to_json(sys.argv[1], sys.argv[2], nested=nested)
