"""Batch file renamer"""
import os
import re

def batch_rename(directory: str, pattern: str, replacement: str, dry_run: bool = True):
    renamed = 0
    for fname in os.listdir(directory):
        if re.search(pattern, fname):
            new_name = re.sub(pattern, replacement, fname)
            old_path = os.path.join(directory, fname)
            new_path = os.path.join(directory, new_name)
            if dry_run:
                print(f"[DRY RUN] {fname} -> {new_name}")
            else:
                os.rename(old_path, new_path)
                print(f"Renamed: {fname} -> {new_name}")
            renamed += 1
    print(f"Total: {renamed} files {'would be' if dry_run else ''} renamed")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: batch_rename.py <dir> <pattern> <replacement> [--execute]")
        sys.exit(1)
    dry = "--execute" not in sys.argv
    batch_rename(sys.argv[1], sys.argv[2], sys.argv[3], dry_run=dry)
