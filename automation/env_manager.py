"""Environment variable manager"""
import os
import json
from typing import Optional

class EnvManager:
    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self.vars = self._load()
    
    def _load(self) -> dict:
        vars = {}
        try:
            with open(self.env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        key, _, val = line.partition("=")
                        vars[key.strip()] = val.strip()
        except FileNotFoundError:
            pass
        return vars
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return os.environ.get(key, self.vars.get(key, default))
    
    def set(self, key: str, value: str):
        self.vars[key] = value
        self._save()
        os.environ[key] = value
    
    def _save(self):
        with open(self.env_file, 'w') as f:
            for key, val in self.vars.items():
                f.write(f"{key}={val}\n")

if __name__ == "__main__":
    env = EnvManager()
    print(f"PATH: {env.get('PATH', 'not set')}")
