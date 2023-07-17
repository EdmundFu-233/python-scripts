"""SSH connection manager"""
import os
import subprocess
from typing import Dict, Optional

class SSHConfig:
    def __init__(self):
        self.config_path = os.path.expanduser("~/.ssh/config")
        self.hosts = self._parse()
    
    def _parse(self) -> Dict:
        hosts = {}
        current_host = None
        try:
            with open(self.config_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("Host "):
                        current_host = line.split()[1]
                        hosts[current_host] = {}
                    elif current_host and "=" in line:
                        key, val = line.split("=", 1)
                        hosts[current_host][key.strip()] = val.strip()
                    elif current_host and line and not line.startswith("#"):
                        parts = line.split()
                        if len(parts) >= 2:
                            hosts[current_host][parts[0].lower()] = parts[1]
        except FileNotFoundError:
            pass
        return hosts
    
    def list_hosts(self) -> list:
        return list(self.hosts.keys())
    
    def connect(self, hostname: str):
        if hostname in self.hosts:
            subprocess.run(["ssh", hostname])
        else:
            print(f"Unknown host: {hostname}")

if __name__ == "__main__":
    config = SSHConfig()
    print("Configured hosts:", config.list_hosts())
