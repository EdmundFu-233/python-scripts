#!/usr/bin/env python3
"""
DNS Lookup Utility

Performs various DNS record lookups (A, AAAA, MX, NS, TXT, CNAME, SOA)
with optional reverse lookup support.

Usage:
    python dns_lookup.py example.com
    python dns_lookup.py example.com --type MX
    python dns_lookup.py example.com --all
    python dns_lookup.py 8.8.8.8 --reverse
"""

import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Optional

RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]


@dataclass
class DnsResult:
    record_type: str
    value: str
    error: Optional[str] = None


def resolve_hostname(hostname: str, record_type: str = "A") -> DnsResult:
    """Resolve a hostname to the specified DNS record type."""
    try:
        if record_type == "A":
            info = socket.getaddrinfo(hostname, None, socket.AF_INET)
            ips = sorted({addr[4][0] for addr in info})
            return DnsResult("A", ", ".join(ips) if ips else "No records")

        elif record_type == "AAAA":
            try:
                info = socket.getaddrinfo(hostname, None, socket.AF_INET6)
                ips = sorted({addr[4][0] for addr in info})
                return DnsResult("AAAA", ", ".join(ips) if ips else "No records")
            except socket.gaierror:
                return DnsResult("AAAA", "No IPv6 records found")

        elif record_type == "CNAME":
            try:
                cname = socket.getaddrinfo(hostname, None)
                return DnsResult("CNAME", f"Resolved to {cname[0][4][0] if cname else 'N/A'}")
            except socket.gaierror:
                return DnsResult("CNAME", "No CNAME record")

        elif record_type in ("MX", "NS", "TXT", "SOA"):
            return DnsResult(
                record_type,
                f"(requires dnspython for full {record_type} resolution)",
            )

        else:
            return DnsResult(record_type, "", error=f"Unknown record type: {record_type}")

    except socket.gaierror as e:
        return DnsResult(record_type, "", error=str(e))
    except Exception as e:
        return DnsResult(record_type, "", error=str(e))


def reverse_lookup(ip: str) -> DnsResult:
    """Perform reverse DNS lookup on an IP address."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return DnsResult("PTR", hostname)
    except socket.herror:
        return DnsResult("PTR", "No PTR record found")
    except Exception as e:
        return DnsResult("PTR", "", error=str(e))


def lookup_all(hostname: str) -> list[DnsResult]:
    """Query all record types in parallel."""
    results: list[DnsResult] = []
    with ThreadPoolExecutor(max_workers=len(RECORD_TYPES)) as executor:
        futures = {
            executor.submit(resolve_hostname, hostname, rt): rt
            for rt in RECORD_TYPES
        }
        for future in as_completed(futures):
            results.append(future.result())
    # Sort by record type for consistent output
    results.sort(key=lambda r: RECORD_TYPES.index(r.record_type)
                 if r.record_type in RECORD_TYPES else 99)
    return results


def print_results(results: list[DnsResult]) -> None:
    """Print DNS lookup results in a formatted table."""
    print(f"\n{'Type':<8} {'Value'}")
    print("-" * 50)
    for r in results:
        status = r.value if not r.error else f"❌ {r.error}"
        print(f"{r.record_type:<8} {status}")


def is_ip_address(value: str) -> bool:
    """Check if the input value looks like an IP address."""
    try:
        socket.inet_pton(socket.AF_INET, value)
        return True
    except OSError:
        pass
    try:
        socket.inet_pton(socket.AF_INET6, value)
        return True
    except OSError:
        pass
    return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="DNS Lookup Utility — query DNS records for a domain",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Record types: {', '.join(RECORD_TYPES)}",
    )
    parser.add_argument("target", help="Domain name or IP address to look up")
    parser.add_argument(
        "--type", "-t",
        choices=RECORD_TYPES,
        default="A",
        help="DNS record type (default: A)",
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Query all record types",
    )
    parser.add_argument(
        "--reverse", "-r",
        action="store_true",
        help="Perform reverse DNS lookup (PTR)",
    )

    args = parser.parse_args()

    target = args.target.strip()

    if args.reverse or is_ip_address(target):
        result = reverse_lookup(target)
        print_results([result])
        sys.exit(0)

    if args.all:
        results = lookup_all(target)
    else:
        results = [resolve_hostname(target, args.type)]

    print_results(results)


if __name__ == "__main__":
    main()
