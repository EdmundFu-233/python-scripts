"""Simple backup tool"""
import os
import shutil
from datetime import datetime

def backup(source: str, dest: str, compress: bool = False):
    if not os.path.exists(source):
        print(f"Source {source} not found")
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"
    dest_path = os.path.join(dest, backup_name)
    if compress:
        shutil.make_archive(dest_path, 'zip', source)
        print(f"Compressed backup: {dest_path}.zip")
    else:
        shutil.copytree(source, dest_path)
        print(f"Backup created: {dest_path}")

if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else "."
    dst = sys.argv[2] if len(sys.argv) > 2 else "./backups"
    backup(src, dst, compress=True)
