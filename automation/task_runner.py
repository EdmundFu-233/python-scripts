"""Task runner with dependency tracking"""
import subprocess
from typing import Dict, List

class Task:
    def __init__(self, name: str, command: str, deps: List[str] = None):
        self.name = name
        self.command = command
        self.deps = deps or []
    
    def run(self) -> bool:
        print(f"Running: {self.name}")
        result = subprocess.run(self.command, shell=True, capture_output=True)
        if result.returncode == 0:
            print(f"  OK: {result.stdout.decode()[:100]}")
            return True
        else:
            print(f"  FAILED: {result.stderr.decode()[:100]}")
            return False

class TaskRunner:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
    
    def add(self, task: Task):
        self.tasks[task.name] = task
    
    def run(self, name: str, visited: set = None) -> bool:
        if visited is None:
            visited = set()
        if name in visited:
            return True
        visited.add(name)
        task = self.tasks.get(name)
        if not task:
            print(f"Task '{name}' not found")
            return False
        for dep in task.deps:
            if not self.run(dep, visited):
                return False
        return task.run()

if __name__ == "__main__":
    runner = TaskRunner()
    runner.add(Task("build", "echo building..."))
    runner.add(Task("test", "echo testing...", deps=["build"]))
    runner.add(Task("deploy", "echo deploying...", deps=["test"]))
    runner.run("deploy")
