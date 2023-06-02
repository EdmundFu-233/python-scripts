"""Ping sweep for network discovery"""
import subprocess
from concurrent.futures import ThreadPoolExecutor

def ping_host(ip: str) -> bool:
    result = subprocess.run(["ping", "-c", "1", "-W", "1", ip],
                          capture_output=True, text=True)
    return result.returncode == 0

def sweep(network: str, start: int, end: int) -> list:
    active = []
    ips = [f"{network}.{i}" for i in range(start, end + 1)]
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(ping_host, ips)
        for ip, alive in zip(ips, results):
            if alive:
                active.append(ip)
                print(f"Host alive: {ip}")
    return active

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: ping_sweep.py <network> <start> <end>")
        print("Example: ping_sweep.py 192.168.1 1 254")
        sys.exit(1)
    sweep(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
