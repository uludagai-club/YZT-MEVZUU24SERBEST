import re
import json
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from extractor import contact_channel_extractor

class KeyValueExtractor:
    def __init__(self,tesseract):
        
        self.tesseract=tesseract
        
        doc_name = "data_extraction/cv_patterns.json"
        with open(doc_name, 'r', encoding="utf-8") as document:
          self.patterns = json.load(document)
          
        self.my_extractor=contact_channel_extractor.TextExtractor()
        
    def extract_info(self):
       
        emails=[]
        domains=[]
        phones=[]
        for field, pattern in self.patterns.items():
            for page_index in self.tesseract.results:
                for section_index in self.tesseract.results[page_index]["sections"]:
                    text=self.tesseract.results[page_index]["sections"][section_index]["text"]
                    
                    email=self.my_extractor.extract_emails(text=text)
                    domain=self.my_extractor.extract_domains(text=text)
                    phone=self.my_extractor.extract_phone_numbers(text=text)
                    
                    emails.extend([x for x in email if x not in emails])
                    domains.extend([x for x in domain if x not in domains])
                    phones.extend([x for x in phone if x not in phones])
                    
                    match = re.search(pattern, text, re.IGNORECASE)

        self.tesseract.results["emails"]=emails
        self.tesseract.results["domains"]=domains
        self.tesseract.results["phones"]=phones
        


