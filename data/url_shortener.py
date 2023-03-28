"""Simple URL shortener"""
import hashlib
import json
from typing import Optional

class URLShortener:
    def __init__(self, storage: str = "links.json"):
        self.storage = storage
        self.links = self._load()
    
    def _load(self) -> dict:
        try:
            with open(self.storage) as f:
                return json.load(f)
        except:
            return {}
    
    def _save(self):
        with open(self.storage, 'w') as f:
            json.dump(self.links, f)
    
    def shorten(self, url: str) -> str:
        key = hashlib.md5(url.encode()).hexdigest()[:8]
        self.links[key] = url
        self._save()
        return key
    
    def resolve(self, key: str) -> Optional[str]:
        return self.links.get(key)

if __name__ == "__main__":
    s = URLShortener()
    key = s.shorten("https://example.com/very/long/url")
    print(f"Shortened: {key}")
    print(f"Resolved: {s.resolve(key)}")
