"""Directory snapshot - track file changes"""
import os
import json
import hashlib
from datetime import datetime

def snapshot(directory: str) -> dict:
    result = {}
    for root, _, files in os.walk(directory):
        for fname in files:
            path = os.path.join(root, fname)
            stat = os.stat(path)
            result[path] = {
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "hash": hashlib.md5(open(path, 'rb').read()).hexdigest()
            }
    return result

if __name__ == "__main__":
    import sys
    snap = snapshot(sys.argv[1] if len(sys.argv) > 1 else ".")
    with open("snapshot.json", 'w') as f:
        json.dump(snap, f, indent=2)
    print(f"Snapshotted {len(snap)} files")
