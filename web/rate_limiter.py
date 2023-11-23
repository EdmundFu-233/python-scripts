"""Token bucket rate limiter"""
import time
import threading

class RateLimiter:
    def __init__(self, rate: float, burst: int):
        self.rate = rate
        self.burst = burst
        self.tokens = burst
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
        self.last_refill = now
    
    def acquire(self, tokens: int = 1) -> bool:
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def wait_and_acquire(self, tokens: int = 1):
        while not self.acquire(tokens):
            time.sleep(0.05)

if __name__ == "__main__":
    limiter = RateLimiter(rate=1.0, burst=5)
    for i in range(10):
        if limiter.acquire():
            print(f"Request {i} allowed")
        else:
            print(f"Request {i} rate limited")
        time.sleep(0.2)
