"""Caesar cipher encryption/decryption"""
def encrypt(text: str, shift: int) -> str:
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26
            result.append(chr(base + shifted))
        else:
            result.append(char)
    return ''.join(result)

def decrypt(text: str, shift: int) -> str:
    return encrypt(text, -shift)

def brute_force(text: str) -> dict:
    results = {}
    for shift in range(26):
        results[shift] = decrypt(text, shift)
    return results

if __name__ == "__main__":
    msg = "Hello, World!"
    encrypted = encrypt(msg, 3)
    decrypted = decrypt(encrypted, 3)
    print(f"Original: {msg}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
