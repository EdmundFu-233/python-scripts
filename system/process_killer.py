"""Find and kill processes by name"""
import os
import signal
import subprocess

def find_process(name: str) -> list:
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    processes = []
    for line in result.stdout.split("\n")[1:]:
        if name.lower() in line.lower():
            parts = line.split()
            if parts:
                processes.append({"pid": int(parts[1]), "user": parts[0], "cmd": " ".join(parts[10:])})
    return processes

def kill_process(pid: int, force: bool = False) -> bool:
    sig = signal.SIGKILL if force else signal.SIGTERM
    try:
        os.kill(pid, sig)
        return True
    except:
        return False

if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else input("Process name: ")
    procs = find_process(name)
    for p in procs:
        print(f"  PID {p['pid']}: {p['cmd'][:60]}")
