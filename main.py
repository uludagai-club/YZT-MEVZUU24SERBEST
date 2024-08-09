from text_recognition.tesseract import Tesseract
from data_extraction.key_value_extraction import KeyValueExtractor
from utils.pdf_to_text import pdf_to_text

class Operator:
    
    def __init__(self,file_path,teseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        self.tesseract_path = teseract_path
        self.file_path=file_path
        self.tesseract=Tesseract(self.tesseract_path,self.file_path)
    
    def do_tesseract_parts(self):
        self.tesseract.get_result_and_purge_blank_texts()
        document_language=self.tesseract.detect_language_via_text()
        
        if document_language=="tur":
            self.tesseract.lang="tur"
            self.tesseract.get_result_and_purge_blank_texts()
            
        self.tesseract.get_punktos()
        self.tesseract.detect_phrases()
        
        #self.tesseract.check_sections_and_line()
        
        self.tesseract.get_rectangles()
        self.tesseract.rectangle_to_text()
        print("aaa")

    
    def get_contact_infos(self):
        self.key_value_extractor=KeyValueExtractor(self.tesseract)
        self.key_value_extractor.extract_info()
        
    def get_university(self):
        print("aaa")
        pass
    
    def check_sections_and_line(self):
        self.file_content = pdf_to_text(self.pdf_file_path)
        lines = self.file_content.split('\n')
        for page_index in self.results:
            for section_index in self.results[page_index]['sections']:

                section_text = self.results[page_index]['sections'][section_index]['text']
                for line_index in range(len(lines)):
                    try:
                        if lines[line_index].find(section_text)!=-1:
                            found_index=line_index
                            lines[found_index] = section_index
                            break
                    except:
                        pass
            for line in lines:
                if type(line)!=int:
                   similarity_results = self.similarity_analayse.get_similarity_text_and_phrase_for_headers(line)
                   if line=="EĞİTİM":
                       print()
                       similarity_results = self.similarity_analayse.get_similarity_text_and_phrase_for_headers(line)
                   if len(similarity_results)!=0:
                       print()
                pass
        
