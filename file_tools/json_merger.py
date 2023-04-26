"""JSON File Merger"""
import json
import glob
from typing import Any

def merge_json_files(pattern: str) -> list:
    merged = []
    for filename in glob.glob(pattern):
        with open(filename) as f:
            data = json.load(f)
            if isinstance(data, list):
                merged.extend(data)
            else:
                merged.append(data)
    return merged

def write_json(data: Any, output: str):
    with open(output, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    import sys
    merged = merge_json_files(sys.argv[1])
    write_json(merged, sys.argv[2])
    print(f"Merged {len(merged)} items")
