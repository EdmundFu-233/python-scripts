"""Check if URLs are accessible"""
import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

def check_url(url: str, timeout: int = 5) -> dict:
    try:
        resp = requests.head(url, timeout=timeout, allow_redirects=True)
        return {"url": url, "status": resp.status_code, "ok": resp.ok,
                "redirects": len(resp.history)}
    except Exception as e:
        return {"url": url, "status": 0, "ok": False, "error": str(e)}

def check_urls(urls: list, max_workers: int = 10) -> list:
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        return list(ex.map(check_url, urls))

if __name__ == "__main__":
    urls = ["https://google.com", "https://github.com", "https://notexist.xyz"]
    for result in check_urls(urls):
        status = result['status']
        icon = "✓" if result['ok'] else "✗"
        print(f"{icon} {result['url']}: {status}")
