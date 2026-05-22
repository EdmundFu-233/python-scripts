#!/usr/bin/env python3
"""JSON diff and patch utility for comparing nested structures."""

import json
from typing import Any, Dict, List, Tuple


def json_diff(a: Any, b: Any, path: str = "$") -> List[Tuple[str, str, Any, Any]]:
    """Compare two JSON values, returning (path, op, old, new) for each difference."""
    changes = []

    if type(a) != type(b):
        changes.append((path, "type_change", a, b))
        return changes

    if isinstance(a, dict):
        all_keys = set(list(a.keys()) + list(b.keys()))
        for key in all_keys:
            child_path = f"{path}.{key}"
            if key not in a:
                changes.append((child_path, "add", None, b[key]))
            elif key not in b:
                changes.append((child_path, "remove", a[key], None))
            else:
                changes.extend(json_diff(a[key], b[key], child_path))

    elif isinstance(a, list):
        max_len = max(len(a), len(b))
        for i in range(max_len):
            child_path = f"{path}[{i}]"
            if i >= len(a):
                changes.append((child_path, "add", None, b[i]))
            elif i >= len(b):
                changes.append((child_path, "remove", a[i], None))
            else:
                changes.extend(json_diff(a[i], b[i], child_path))

    elif a != b:
        changes.append((path, "modify", a, b))

    return changes


def apply_patch(obj: Any, patch: List[Tuple[str, str, Any, Any]]) -> Any:
    """Apply a list of diffs to a JSON object (destructive merge)."""
    import copy
    result = copy.deepcopy(obj)

    for path, op, old, new in patch:
        if op == "modify":
            parts = path.split(".")
            target = result
            for p in parts[1:-1]:
                target = target[p]
            target[parts[-1]] = new

    return result


if __name__ == "__main__":
    a = {"name": "Alice", "age": 30, "tags": ["dev"]}
    b = {"name": "Alice", "age": 31, "tags": ["dev", "ops"], "level": "senior"}
    diffs = json_diff(a, b)
    for d in diffs:
        print(f"  {d[0]}: {d[1]} ({d[2]} -> {d[3]})")
