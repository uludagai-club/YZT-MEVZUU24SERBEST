import re

def clean_text(text,language):
    # Alphanumeric characters and extra whitespaces removal
    cleaned_text = re.sub(r'[^\w\sğüşöçıİĞÜŞÖÇ]', '', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    if language=="tr" or language=="tur":
        cleaned_text = turkish_lower(cleaned_text)
    else:
        cleaned_text = cleaned_text.lower()
    return cleaned_text

def turkish_lower(text):
    # Turkish lowercase conversion with special handling for 'I'
    turkish_chars = {'İ': 'i', 'I': 'ı', 'Ç': 'ç', 'Ğ': 'ğ', 'Ö': 'ö', 'Ü': 'ü', 'Ş': 'ş'}
    text = ''.join(turkish_chars.get(c, c) for c in text)
    text = text.lower()
    return text
if __name__=="__main__":
    text = "EĞİTİM"
    cleaned_text = clean_text(text,"tr")
    print(cleaned_text)
