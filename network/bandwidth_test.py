"""Simple bandwidth test"""
import time
import socket

def test_download_speed(url: str = "http://speedtest.tele2.net/1MB.zip") -> float:
    import requests
    start = time.time()
    resp = requests.get(url, stream=True)
    downloaded = 0
    for chunk in resp.iter_content(chunk_size=8192):
        if chunk:
            downloaded += len(chunk)
    elapsed = time.time() - start
    speed = (downloaded / elapsed) / (1024 * 1024)  # MB/s
    return speed

def measure_latency(host: str = "8.8.8.8", port: int = 53, count: int = 5) -> dict:
    times = []
    for _ in range(count):
        start = time.time()
        try:
            socket.create_connection((host, port), timeout=2)
            times.append((time.time() - start) * 1000)
        except:
            pass
    if times:
        return {"min": min(times), "avg": sum(times)/len(times), "max": max(times)}
    return {"error": "no response"}

if __name__ == "__main__":
    print("Testing latency...")
    print(measure_latency())
