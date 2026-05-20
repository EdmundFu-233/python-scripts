#!/usr/bin/env python3
"""Async TCP port scanner with service detection."""

import asyncio
import socket
from typing import List, Tuple


async def scan_port(host: str, port: int, timeout: float = 1.0) -> Tuple[int, str, bool]:
    """Scan a single TCP port."""
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout
        )
        service = socket.getservbyport(port, "tcp") if port < 65536 else "unknown"
        writer.close()
        await writer.wait_closed()
        return port, service, True
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return port, "", False


async def scan_ports(host: str, ports: List[int]) -> List[Tuple[int, str]]:
    """Scan multiple ports concurrently."""
    tasks = [scan_port(host, p) for p in ports]
    results = await asyncio.gather(*tasks)
    return [(p, s) for p, s, ok in results if ok]


def discover_hosts(subnet: str, timeout: float = 0.5) -> List[str]:
    """Ping sweep to discover live hosts on a subnet (e.g., 192.168.1.0/24)."""
    import ipaddress
    import subprocess

    network = ipaddress.ip_network(subnet, strict=False)
    alive = []
    for ip in network.hosts():
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(int(timeout)), str(ip)],
            capture_output=True, text=True, timeout=timeout + 1
        )
        if result.returncode == 0:
            alive.append(str(ip))
    return alive


if __name__ == "__main__":
    import sys
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    ports = list(range(1, 1024))
    open_ports = asyncio.run(scan_ports(host, ports))
    for port, service in open_ports:
        print(f"  {port}/tcp  {service}")
    print(f"Found {len(open_ports)} open ports on {host}")

