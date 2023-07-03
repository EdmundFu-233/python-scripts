"""System resource monitor"""
import os
import time

def get_cpu_usage() -> float:
    with open('/proc/stat') as f:
        fields = f.readline().split()
    total = sum(int(f) for f in fields[1:])
    idle = int(fields[4])
    return (1 - idle / total) * 100

def get_memory_usage() -> dict:
    with open('/proc/meminfo') as f:
        lines = f.readlines()
    total = int(lines[0].split()[1])
    free = int(lines[1].split()[1])
    return {"total_mb": total // 1024, "free_mb": free // 1024,
            "used_pct": (1 - free / total) * 100}

def get_disk_usage(path: str = "/") -> dict:
    stat = os.statvfs(path)
    total = stat.f_frsize * stat.f_blocks
    free = stat.f_frsize * stat.f_bfree
    return {"total_gb": total // (1024**3), "free_gb": free // (1024**3),
            "used_pct": (1 - free / total) * 100}

if __name__ == "__main__":
    print("CPU:", get_cpu_usage())
    print("Memory:", get_memory_usage())
    print("Disk:", get_disk_usage())
