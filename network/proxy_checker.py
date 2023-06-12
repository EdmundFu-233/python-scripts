"""Check if proxies are working"""
import requests
from concurrent.futures import ThreadPoolExecutor

def check_proxy(proxy: str, timeout: int = 5) -> bool:
    proxies = {"http": proxy, "https": proxy}
    try:
        resp = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=timeout)
        return resp.status_code == 200
    except:
        return False

def check_proxies(proxy_list: list) -> list:
    working = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(check_proxy, proxy_list)
        for proxy, alive in zip(proxy_list, results):
            if alive:
                working.append(proxy)
                print(f"Working: {proxy}")
    return working

if __name__ == "__main__":
    proxies = ["http://proxy1:8080", "http://proxy2:8080"]
    check_proxies(proxies)
