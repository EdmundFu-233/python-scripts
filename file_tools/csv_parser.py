"""CSV Parser - parse and analyze CSV files"""
import csv
from typing import List, Dict

def read_csv(filepath: str) -> List[Dict[str, str]]:
    with open(filepath, 'r') as f:
        return list(csv.DictReader(f))

def column_stats(data: List[Dict], col: str) -> dict:
    values = [float(row[col]) for row in data if row[col]]
    return {
        "min": min(values), "max": max(values),
        "avg": sum(values) / len(values),
        "count": len(values)
    }

if __name__ == "__main__":
    import sys
    data = read_csv(sys.argv[1])
    print(f"Loaded {len(data)} rows")
    for key in data[0]:
        try:
            stats = column_stats(data, key)
            print(f"{key}: {stats}")
        except:
            pass
