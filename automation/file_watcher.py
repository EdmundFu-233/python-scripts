"""Watch directory for file changes"""
import os
import time
from hashlib import md5

class FileWatcher:
    def __init__(self, directory: str, callback=None):
        self.directory = directory
        self.callback = callback
        self.file_hashes = {}
    
    def scan(self):
        current = {}
        for root, _, files in os.walk(self.directory):
            for fname in files:
                path = os.path.join(root, fname)
                with open(path, 'rb') as f:
                    current[path] = md5(f.read()).hexdigest()
        return current
    
    def watch(self, interval: float = 1.0):
        self.file_hashes = self.scan()
        try:
            while True:
                time.sleep(interval)
                current = self.scan()
                for path in current:
                    if path not in self.file_hashes:
                        print(f"New file: {path}")
                    elif current[path] != self.file_hashes[path]:
                        print(f"Modified: {path}")
                for path in self.file_hashes:
                    if path not in current:
                        print(f"Deleted: {path}")
                self.file_hashes = current
        except KeyboardInterrupt:
            print("Watcher stopped")

if __name__ == "__main__":
    w = FileWatcher(".")
    w.watch()
