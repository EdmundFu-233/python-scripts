"""Date utility functions"""
from datetime import datetime, timedelta
from typing import List

def date_range(start: str, end: str, fmt="%Y-%m-%d") -> List[str]:
    start_dt = datetime.strptime(start, fmt)
    end_dt = datetime.strptime(end, fmt)
    dates = []
    current = start_dt
    while current <= end_dt:
        dates.append(current.strftime(fmt))
        current += timedelta(days=1)
    return dates

def days_between(start: str, end: str, fmt="%Y-%m-%d") -> int:
    start_dt = datetime.strptime(start, fmt)
    end_dt = datetime.strptime(end, fmt)
    return (end_dt - start_dt).days

def is_weekend(date_str: str, fmt="%Y-%m-%d") -> bool:
    dt = datetime.strptime(date_str, fmt)
    return dt.weekday() >= 5

if __name__ == "__main__":
    print(date_range("2023-01-01", "2023-01-07"))
