"""Get IP information"""
import socket
import requests

def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def get_public_ip() -> str:
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Unknown"

def whois_lookup(domain: str) -> dict:
    import subprocess
    result = subprocess.run(["whois", domain], capture_output=True, text=True)
    lines = result.stdout.split("\n")[:20]
    info = {}
    for line in lines:
        if ":" in line:
            key, _, val = line.partition(":")
            info[key.strip()] = val.strip()
    return info

if __name__ == "__main__":
    print(f"Local IP: {get_local_ip()}")
    print(f"Public IP: {get_public_ip()}")
