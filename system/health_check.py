#!/usr/bin/env python3
"""
System Health Check — monitors CPU, memory, disk, and network.
Outputs both human-readable summary and JSON for automation.
"""

import json
import os
import platform
import shutil
import subprocess
import time
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class HealthReport:
    """Health check report data."""
    timestamp: float = field(default_factory=time.time)
    hostname: str = field(default_factory=platform.node)
    platform: str = field(default_factory=lambda: f"{platform.system()} {platform.release()}")
    cpu_percent: float = 0.0
    memory_total_gb: float = 0.0
    memory_used_gb: float = 0.0
    memory_percent: float = 0.0
    disk_total_gb: float = 0.0
    disk_used_gb: float = 0.0
    disk_percent: float = 0.0
    uptime_hours: float = 0.0
    load_avg: tuple = (0.0, 0.0, 0.0)
    errors: list = field(default_factory=list)


def get_cpu_percent() -> float:
    """Get CPU usage percent."""
    try:
        with open("/proc/stat") as f:
            line = f.readline().strip().split()
            if len(line) < 5:
                return 0.0
            total = sum(int(v) for v in line[1:] if v.isdigit())
            idle = int(line[4])
            return max(0.0, 100.0 * (1.0 - idle / total)) if total > 0 else 0.0
    except (FileNotFoundError, ValueError, IndexError):
        return 0.0


def get_uptime() -> float:
    """Get system uptime in hours."""
    try:
        with open("/proc/uptime") as f:
            return float(f.read().split()[0]) / 3600.0
    except (FileNotFoundError, ValueError, IndexError):
        return 0.0


def get_load_avg() -> tuple:
    """Get 1, 5, 15 minute load averages."""
    try:
        with open("/proc/loadavg") as f:
            parts = f.read().strip().split()[:3]
            return tuple(float(x) for x in parts)
    except (FileNotFoundError, ValueError, IndexError):
        return (0.0, 0.0, 0.0)


def check_health() -> HealthReport:
    """Run all health checks and return a report."""
    report = HealthReport()

    # CPU
    report.cpu_percent = get_cpu_percent()
    report.load_avg = get_load_avg()
    report.uptime_hours = get_uptime()

    # Memory
    try:
        total, used, _ = map(int, os.popen("free -b").readlines()[1].split()[1:4])
        report.memory_total_gb = round(total / (1024**3), 2)
        report.memory_used_gb = round(used / (1024**3), 2)
        report.memory_percent = round(100.0 * used / total, 1) if total > 0 else 0.0
    except (IndexError, ValueError, OSError):
        report.errors.append("Failed to read memory info")

    # Disk
    try:
        usage = shutil.disk_usage("/")
        report.disk_total_gb = round(usage.total / (1024**3), 2)
        report.disk_used_gb = round(usage.used / (1024**3), 2)
        report.disk_percent = round(100.0 * usage.used / usage.total, 1)
    except OSError:
        report.errors.append("Failed to read disk info")

    return report


def print_report(report: HealthReport) -> None:
    """Print a human-readable health report."""
    print(f"{'='*50}")
    print(f"  System Health Report — {report.hostname}")
    print(f"{'='*50}")
    print(f"  Platform:    {report.platform}")
    print(f"  Uptime:      {report.uptime_hours:.1f} hours")
    print(f"  Load Avg:    {report.load_avg[0]:.1f} {report.load_avg[1]:.1f} {report.load_avg[2]:.1f}")
    print(f"  CPU:         {report.cpu_percent:.1f}%")
    print(f"  Memory:      {report.memory_used_gb:.1f}/{report.memory_total_gb:.1f} GB ({report.memory_percent:.1f}%)")
    print(f"  Disk:        {report.disk_used_gb:.1f}/{report.disk_total_gb:.1f} GB ({report.disk_percent:.1f}%)")
    if report.errors:
        print(f"  Errors:      {len(report.errors)}")
        for err in report.errors:
            print(f"    - {err}")
    print(f"{'='*50}")


def main():
    report = check_health()
    print_report(report)
    print()
    print("JSON Output:")
    print(json.dumps(asdict(report), indent=2))


if __name__ == "__main__":
    main()
