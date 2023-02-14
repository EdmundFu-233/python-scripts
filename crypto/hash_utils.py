"""Hashing utilities"""
import hashlib
import hmac

def hash_file(filepath: str, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            h.update(chunk)
    return h.hexdigest()

def hash_string(text: str, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    h.update(text.encode())
    return h.hexdigest()

def hmac_sign(message: str, secret: str) -> str:
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()

def verify_hmac(message: str, secret: str, signature: str) -> bool:
    expected = hmac_sign(message, secret)
    return hmac.compare_digest(expected, signature)

if __name__ == "__main__":
    print("SHA256:", hash_string("hello"))
    sig = hmac_sign("message", "secret")
    print("HMAC:", sig)
    print("Verify:", verify_hmac("message", "secret", sig))
