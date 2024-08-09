import re
import tldextract
import json
import fuzzywuzzy.fuzz as fuzz

class TextExtractor:
    def __init__(self):
        self.email_regex = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,3}")
        self.phone_regex = re.compile(r"(?<!\d)(\+90|0)?\s*(\(\d{3}\)[\s-]\d{3}[\s-]\d{2}[\s-]\d{2}|\(\d{3}\)[\s-]\d{3}[\s-]\d{4}|\(\d{3}\)[\s-]\d{7}|\d{3}[\s-]\d{3}[\s-]\d{4}|\d{3}[\s-]\d{3}[\s-]\d{2}[\s-]*\d{2})(?!\d)")
        self.universities_parts=["University","Üniversite"]
        
        self.extractor = tldextract.TLDExtract()
        self.universities={}
        with open("utils/universities.json","r",encoding="utf-8") as f:
            self.universities = json.load(f)

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
    
    def extract_university(self,text,threshold=0.80):
        for item in self.universities:
            university_name = item['University']
            similarity = fuzz.ratio(text, university_name) / 100
            if similarity >= threshold:
                return item
            
            for university_part in university_name.split(" "):
                similarity = fuzz.ratio(text, university_part) / 100
                if similarity >= threshold:
                    return item

            seperated_texts=text.split(" ")
            for seperated_text in seperated_texts:
                for universities_part in self.universities_parts:
                    similarity = fuzz.ratio(universities_part, seperated_text) / 100
                    if similarity >= threshold:
                        return  {
                            "University": text,
                            "Global Rank": None,
                            "Global Score": None,
                            "State": None
                            }
                
            
        return None