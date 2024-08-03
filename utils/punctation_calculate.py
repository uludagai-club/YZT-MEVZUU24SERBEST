import string

def calculate_punctuation_ratio(text):
    punctuation_chars = string.punctuation + "$%₺€æß©"
    punctuation_count = sum(1 for char in text if char in punctuation_chars)
    return punctuation_count / len(text) if len(text) != 0 else 1

