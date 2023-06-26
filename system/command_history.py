"""Search command history"""
import os
from collections import Counter
from typing import List

class HistorySearch:
    def __init__(self, history_file: str = None):
        if history_file is None:
            history_file = os.path.expanduser("~/.bash_history")
        self.history_file = history_file
        self.commands = self._load()
    
    def _load(self) -> List[str]:
        try:
            with open(self.history_file, 'r', errors='ignore') as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return []
    
    def search(self, query: str, max_results: int = 20) -> List[str]:
        results = [c for c in self.commands if query.lower() in c.lower()]
        return results[:max_results]
    
    def top_commands(self, n: int = 10) -> List[tuple]:
        return Counter(self.commands).most_common(n)
    
    def stats(self) -> dict:
        return {
            "total_commands": len(self.commands),
            "unique_commands": len(set(self.commands)),
            "most_used": self.top_commands(5)
        }

if __name__ == "__main__":
    h = HistorySearch()
    print("Stats:", h.stats())
    query = input("Search: ")
    for cmd in h.search(query):
        print(f"  {cmd}")
