"""Base64 encoding utilities"""
import base64

def encode(text: str) -> str:
    return base64.b64encode(text.encode()).decode()

def decode(encoded: str) -> str:
    return base64.b64decode(encoded).decode()

def encode_file(filepath: str) -> str:
    with open(filepath, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def decode_to_file(encoded: str, filepath: str):
    with open(filepath, 'wb') as f:
        f.write(base64.b64decode(encoded))

if __name__ == "__main__":
    original = "Hello, World!"
    encoded = encode(original)
    decoded = decode(encoded)
    print(f"Original: {original}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")
