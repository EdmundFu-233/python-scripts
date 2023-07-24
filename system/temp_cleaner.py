"""Clean temporary files"""
import os
import shutil
import tempfile
import glob

def clean_temp_files(dry_run: bool = True) -> dict:
    cleaned = {"files": 0, "bytes": 0, "dirs": 0}
    
    patterns = ["*.tmp", "*.log", "*.cache", "__pycache__", ".DS_Store"]
    for pattern in patterns:
        for path in glob.glob(f"**/{pattern}", recursive=True):
            if dry_run:
                print(f"[DRY] Would remove: {path}")
            else:
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                        cleaned["dirs"] += 1
                    else:
                        cleaned["bytes"] += os.path.getsize(path)
                        os.remove(path)
                        cleaned["files"] += 1
                except:
                    pass
    return cleaned

if __name__ == "__main__":
    result = clean_temp_files(dry_run=True)
    print(f"Would clean: {result}")
