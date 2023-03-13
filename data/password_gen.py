"""Secure password generator"""
import random
import string

def generate_password(length: int = 16, use_symbols: bool = True) -> str:
    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def generate_passphrases(num: int = 5, words_per: int = 4) -> list:
    word_list = ["correct", "horse", "battery", "staple", "quantum",
                 "pizza", "dragon", "knight", "river", "stone",
                 "cloud", "ocean", "forest", "thunder", "silver"]
    phrases = []
    for _ in range(num):
        phrase = "-".join(random.choice(word_list) for _ in range(words_per))
        phrases.append(phrase)
    return phrases

if __name__ == "__main__":
    print("Random password:", generate_password())
    print("Passphrases:", generate_passphrases())
