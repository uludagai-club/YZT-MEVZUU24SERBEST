import re
import tldextract

class TextExtractor:
    def __init__(self):
        self.email_regex = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,3}")
        self.phone_regex = re.compile(r"(?<!\d)(\+90|0)?\s*(\(\d{3}\)[\s-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}|\(\d{3}\)[\s-]*\d{3}[\s-]*\d{4}|\(\d{3}\)[\s-]*\d{7}|\d{3}[\s-]*\d{3}[\s-]*\d{4}|\d{3}[\s-]*\d{3}[\s-]*\d{2}[\s-]*\d{2})(?!\d)")

        self.extractor = tldextract.TLDExtract()

    def extract_emails(self, text):
        emails = self.email_regex.findall(text)
        return emails

    def extract_domains(self, text):
        domains = set()
        for url in text.split():
            extracted = self.extractor(url)
            if extracted.domain and extracted.suffix:
                domain = f"{extracted.domain}.{extracted.suffix}"
                domains.add(domain)
        return domains

    def extract_phone_numbers(self, text):
        phones = self.phone_regex.findall(text)
        formatted_phones = []
        for phone in phones:
            second_part = re.sub(r"\D", "", phone[1])  # Remove non-digit characters
            formatted_phones.append(second_part)
        return formatted_phones
