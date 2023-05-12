"""Text file statistics"""
import os
from collections import Counter

def text_stats(filepath: str) -> dict:
    lines = words = chars = 0
    word_freq = Counter()
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        for line in f:
            lines += 1
            chars += len(line)
            tokens = line.split()
            words += len(tokens)
            word_freq.update(t.lower().strip('.,!?;:') for t in tokens)
    return {
        "lines": lines, "words": words, "chars": chars,
        "avg_word_length": chars / max(words, 1),
        "top_words": word_freq.most_common(10)
    }

if __name__ == "__main__":
    import sys
    stats = text_stats(sys.argv[1])
    for k, v in stats.items():
        print(f"{k}: {v}")
