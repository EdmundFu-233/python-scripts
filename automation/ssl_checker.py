#!/usr/bin/env python3
"""
SSL Certificate Checker — monitor SSL/TLS certificate expiry.

Usage:
    python ssl_checker.py example.com
    python ssl_checker.py example.com google.com github.com
    cat domains.txt | python ssl_checker.py

Outputs days until expiry and warning for certificates expiring soon.
Returns exit code 1 if any certificate expires within 14 days.
"""

import ssl
import socket
import sys
import datetime
import argparse


def check_certificate(hostname: str, port: int = 443, timeout: int = 10) -> dict:
    """
    Connect to hostname:port and retrieve SSL certificate info.
    Returns a dict with certificate details or error message.
    """
    result = {"hostname": hostname, "error": None}

    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as tls:
                cert = tls.getpeercert()

                if not cert:
                    result["error"] = "No certificate returned"
                    return result

                # Parse subject
                subject = dict(x[0] for x in cert.get("subject", []))
                result["subject"] = subject.get("commonName", "unknown")
                result["issuer"] = dict(x[0] for x in cert.get("issuer", [])).get(
                    "commonName", "unknown"
                )
                result["serial"] = cert.get("serialNumber", "N/A")

                # Parse validity
                not_before = datetime.datetime.strptime(
                    cert["notBefore"], "%b %d %H:%M:%S %Y %Z"
                )
                not_after = datetime.datetime.strptime(
                    cert["notAfter"], "%b %d %H:%M:%S %Y %Z"
                )

                now = datetime.datetime.utcnow()
                result["not_before"] = not_before.isoformat()
                result["not_after"] = not_after.isoformat()
                result["days_remaining"] = (not_after - now).days
                result["valid"] = not_before <= now <= not_after

                # SANs
                sans = []
                for ext in cert.get("subjectAltName", []):
                    sans.append(ext[1])
                result["sans"] = sans

    except socket.timeout:
        result["error"] = f"Connection to {hostname}:{port} timed out"
    except socket.gaierror:
        result["error"] = f"Could not resolve {hostname}"
    except ConnectionRefusedError:
        result["error"] = f"Connection refused by {hostname}:{port}"
    except ssl.SSLCertVerificationError as e:
        result["error"] = f"SSL verification failed: {e}"
    except Exception as e:
        result["error"] = str(e)

    return result


def format_result(result: dict) -> str:
    """Format certificate check result for display."""
    if result["error"]:
        return f"❌ {result['hostname']}: {result['error']}"

    status = "✅" if result["valid"] else "❌"
    expiry = result["days_remaining"]

    if expiry < 0:
        expiry_str = f"EXPIRED {abs(expiry)} days ago"
    elif expiry == 0:
        expiry_str = "Expires TODAY"
    elif expiry <= 7:
        expiry_str = f"⚠️  {expiry} days (CRITICAL)"
    elif expiry <= 14:
        expiry_str = f"⚠️  {expiry} days (WARNING)"
    elif expiry <= 30:
        expiry_str = f"{expiry} days (soon)"
    else:
        expiry_str = f"{expiry} days"

    return (
        f"{status} {result['hostname']}\n"
        f"   Subject: {result['subject']}\n"
        f"   Issuer:  {result['issuer']}\n"
        f"   Expiry:  {expiry_str}\n"
        f"   Valid:   {result['not_before']} ~ {result['not_after']}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="SSL certificate expiry checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s example.com\n"
            "  %(prog)s example.com google.com\n"
            "  cat domains.txt | %(prog)s\n"
        ),
    )
    parser.add_argument(
        "domains",
        nargs="*",
        help="Domain names to check (or read from stdin)",
    )
    parser.add_argument(
        "-w",
        "--warn-days",
        type=int,
        default=14,
        help="Warning threshold in days (default: 14)",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=10,
        help="Connection timeout in seconds (default: 10)",
    )

    args = parser.parse_args()

    # Collect domains from args or stdin
    domains = args.domains
    if not domains:
        stdin_input = sys.stdin.read().strip()
        if stdin_input:
            domains = [d.strip() for d in stdin_input.splitlines() if d.strip()]

    if not domains:
        parser.print_help()
        sys.exit(1)

    has_warning = False
    for domain in domains:
        result = check_certificate(domain, timeout=args.timeout)
        print(format_result(result))
        print()

        if result.get("days_remaining") is not None:
            if result["days_remaining"] < args.warn_days:
                has_warning = True

    sys.exit(1 if has_warning else 0)


if __name__ == "__main__":
    main()
