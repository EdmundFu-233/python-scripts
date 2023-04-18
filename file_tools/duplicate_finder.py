"""Find duplicate files in directory"""
import os
import hashlib
from collections import defaultdict

def hash_file(filepath: str) -> str:
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(directory: str) -> dict:
    hashes = defaultdict(list)
    for root, _, files in os.walk(directory):
        for fname in files:
            path = os.path.join(root, fname)
            try:
                fhash = hash_file(path)
                hashes[fhash].append(path)
            except:
                pass
    return {h: paths for h, paths in hashes.items() if len(paths) > 1}

if __name__ == "__main__":
    import sys
    dups = find_duplicates(sys.argv[1])
    for h, paths in dups.items():
        print(f"Duplicate ({len(paths)} copies):")
        for p in paths:
            print(f"  {p}")
