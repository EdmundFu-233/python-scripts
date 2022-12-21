"""Simple download manager"""
import os
import requests
from threading import Thread
from queue import Queue

class DownloadManager:
    def __init__(self, max_threads: int = 4):
        self.queue = Queue()
        self.max_threads = max_threads
    
    def add_download(self, url: str, dest: str):
        self.queue.put((url, dest))
    
    def _worker(self):
        while not self.queue.empty():
            url, dest = self.queue.get()
            try:
                resp = requests.get(url, stream=True)
                with open(dest, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded: {dest}")
            except Exception as e:
                print(f"Failed {url}: {e}")
            finally:
                self.queue.task_done()
    
    def start(self):
        threads = []
        for _ in range(min(self.max_threads, self.queue.qsize())):
            t = Thread(target=self._worker)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

if __name__ == "__main__":
    dm = DownloadManager()
    dm.add_download("https://example.com/file.zip", "file.zip")
    dm.start()
