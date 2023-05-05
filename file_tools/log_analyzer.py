"""Log file analyzer - extract errors and patterns"""
import re
from collections import Counter
from typing import List

def analyze_log(filepath: str) -> dict:
    errors = []
    ips = []
    with open(filepath) as f:
        for line in f:
            if 'ERROR' in line or 'error' in line:
                errors.append(line.strip())
            ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
            if ip_match:
                ips.append(ip_match.group())
    return {
        "total_lines": sum(1 for _ in open(filepath)),
        "error_count": len(errors),
        "top_errors": Counter(errors).most_common(5),
        "top_ips": Counter(ips).most_common(10)
    }

if __name__ == "__main__":
    import sys
    result = analyze_log(sys.argv[1])
    for k, v in result.items():
        print(f"{k}: {v}")
