"""Utility module 14"""
import os
import sys
from typing import Optional

def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(key, default)

def get_python_version() -> str:
    return sys.version

def is_python_3() -> bool:
    return sys.version_info.major >= 3

def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(get_python_version())
