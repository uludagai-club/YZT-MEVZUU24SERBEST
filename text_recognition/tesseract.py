import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from datetime import datetime
import json

from text_recognition import rectangle_calculator
from random import randint
import pytesseract


from utils.pdf_to_image import Pdf_to_image
from utils.languagageDetect import LanguageDetect
from utils.similarity_analyse import Similarity_Analayse
from utils.clean_text import clean_text
from utils.detect_punkto import DetectPunkto
from utils.punctation_calculate import calculate_punctuation_ratio
max_punktaiton_ratio=0.75
from utils import concrete_spaced_text
from utils.pdf_to_text import pdf_to_text

class Tesseract:
    
    def __init__(self,tesseract_file_path="",pdf_file_path="",lang="en") -> None:
        if tesseract_file_path!="":
            pytesseract.pytesseract.tesseract_cmd = tesseract_file_path
            self.lang=lang
            self.similarity_analayse=Similarity_Analayse(0.85)
            self.header=dict()
            self.results=dict()
            self.pdf_file_path=pdf_file_path

            self.pdf_to_image=Pdf_to_image(self.pdf_file_path)
            self.pages=self.pdf_to_image.get_pages()
            self.tesseract_result=dict()
            self.languageDetect=LanguageDetect()
            self.myDetectPunkto=DetectPunkto()
    
    def random_color(self):
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)
    
    def detect_language_via_text(self):
        lang_result=[]
        for page_index in self.results:
            sections=self.results[page_index]["sections"]
            for index in sections:
                section_text=self.results[page_index]["sections"][index]["text"]
                lang_result.append(self.languageDetect.detectLanguage(section_text))
        
        return max(set(lang_result), key = lang_result.count)
    
        
    def detect_near_sections(self,page_index):
        will_append=dict()
        for index in self.results[page_index]["sections"]:
            will_append[index]=[]
            main_x1,main_y1,main_x2,main_y2=self.results[page_index]["sections"][index]["rectangle"]
            for second_index in self.results[page_index]["sections"]:
                if index>=second_index:
                    continue
                try:    
                    second_x1,second_y1,second_x2,second_y2=self.results[page_index]["sections"][second_index]["rectangle"]
                    if (main_x2-25<=second_x1 and second_x1<=main_x2+25 ) and (main_y1-10<=second_y1 and second_y1<=main_y1+10):
                        will_append[index].append(second_index)
                        main_x1,main_y1,main_x2,main_y2=second_x1,second_y1,second_x2,second_y2
                    
                    elif (main_y2-25<=second_y1 and second_y1<=main_y2+25 ) and (main_x1-10<=second_x1 and second_x1<=main_x1+10):
                        will_append[index].append(second_index)
                        main_x1,main_y1,main_x2,main_y2=second_x1,second_y1,second_x2,second_y2
                except:
                    pass
        return will_append
                        
    def find_will_be_removed_indexs(self,page_index,will_append):
        will_be_removed_indexs=[]
        for index in will_append:
            if index not in will_be_removed_indexs:
                for add_index in will_append[index]:
                    
                    will_be_removed_indexs.append(add_index) if add_index not in will_be_removed_indexs else will_be_removed_indexs
                    
                    main_text=self.results[page_index]["sections"][index]["text"]
                    second_text=self.results[page_index]["sections"][add_index]["text"]
                    new_text=main_text+" "+second_text
                    self.results[page_index]["sections"][index]["text"]=new_text
                    
                    main_x1,main_y1,main_x2,main_y2=self.results[page_index]["sections"][index]["rectangle"]
                    second_x1,second_y1,second_x2,second_y2=self.results[page_index]["sections"][add_index]["rectangle"]
                    
                    x1,y1,x2,y2=(min(main_x1,second_x1),min(main_y1,second_y1),max(main_x2,second_x2),max(main_y2,second_y2))
                    self.results[page_index]["sections"][index]["rectangle"]=(x1,y1,x2,y2)
                    
        return will_be_removed_indexs
        
    def get_result_and_purge_blank_texts(self):
        # import shutil
        # shutil.rmtree("crops")
        # os.makedirs("crops")
        for page,page_index in zip(self.pages,range(len(self.pages))):
            self.results[page_index]={"sections":{},"bigger_sections":{}}
            self.tesseract_result[page_index]=pytesseract.image_to_data(page, output_type = pytesseract.Output.DICT, lang=self.lang)
            will_be_removed_indexs=[]
            
            for text,index in zip(self.tesseract_result[page_index]["text"],range(len(self.tesseract_result[page_index]["width"]))):
                
                # left=self.tesseract_result[page_index]["left"][index]
                # right=left+self.tesseract_result[page_index]["width"][index]
                # top=self.tesseract_result[page_index]["top"][index]
                # bottom=top+self.tesseract_result[page_index]["height"][index]
                
                # rectangle=(left,top,right,bottom)
                
                # rectangle_image=page.crop(rectangle)
                
                # try:
                #     rectangle_image.save(f"crops/{text}_{index}.png")
                # except:
                #     pass
                
                if len(text.strip())==0:
                    will_be_removed_indexs.append(index)
               
            counter=0    
            for remove_index in will_be_removed_indexs:
                for list_key in self.tesseract_result[page_index]:
                    if type(self.tesseract_result[page_index][list_key])==list:
                        self.tesseract_result[page_index][list_key].pop(remove_index-counter)
                counter+=1
                
            for text,index in zip(self.tesseract_result[page_index]["text"],range(len(self.tesseract_result[page_index]["width"]))):                
                left=self.tesseract_result[page_index]["left"][index]
                right=left+self.tesseract_result[page_index]["width"][index]
                top=self.tesseract_result[page_index]["top"][index]
                bottom=top+self.tesseract_result[page_index]["height"][index]
                
                self.results[page_index]["sections"][index]={"text":text, 
                                                            "rectangle":(left,top,right,bottom)}

            will_append=self.detect_near_sections(page_index)
            will_be_removed_indexs=self.find_will_be_removed_indexs(page_index,will_append)            
            
            
            for remove_index in will_be_removed_indexs:
                self.results[page_index]["sections"].pop(remove_index)     
                
            will_append=self.detect_near_sections(page_index)
            will_be_removed_indexs=self.find_will_be_removed_indexs(page_index,will_append)            
            
            for remove_index in will_be_removed_indexs:
                self.results[page_index]["sections"].pop(remove_index)

            
    def get_punktos(self):
        
        for page_index in range(len(self.pages)):
            
            self.tesseract_result[page_index]["punktos"]=[]
            for height,text in zip(self.tesseract_result[page_index]["height"],self.tesseract_result[page_index]["text"]):

                self.tesseract_result[page_index]["punktos"].append(height)
        
    def detect_phrases(self):
        for page_index in range(len(self.tesseract_result)):
        
            self.tesseract_result[page_index]["bigger_punkto"]=self.myDetectPunkto.detect_big_punkto(self.tesseract_result[page_index]["punktos"])
            for section_index in self.results[page_index]["sections"]:
                
                punkto=self.tesseract_result[page_index]["punktos"][section_index]
                self.results[page_index]["sections"][section_index]["text"]=concrete_spaced_text.main(self.results[page_index]["sections"][section_index]["text"])
                text=self.results[page_index]["sections"][section_index]["text"]
                rectangle=self.results[page_index]["sections"][section_index]["rectangle"]
    
                if calculate_punctuation_ratio(text=text)<max_punktaiton_ratio:
                    phrase_result=self.similarity_analayse.get_similarity_text_and_phrase_for_headers(clean_text(text=text,language=self.lang))
                    if len(phrase_result)!=0:
                        self.results[page_index]["bigger_sections"][section_index]={"text":text, 
                                                                    "phrase":phrase_result,
                                                                    "rectangle":rectangle}
    
    def check_sections_and_line(self):
        self.file_content = pdf_to_text(self.pdf_file_path)
        lines = self.file_content.split('\n')
        for page_index in self.results:
            last_section_index=0
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
                last_section_index=section_index
                
            last_section_index+=1 
            for line_index in range(len(lines)):
                line=lines[line_index]
                if type(line)!=int:
                    
                    after_section_index=lines[line_index+1]
                    after_section=self.results[page_index]["sections"][after_section_index]
                    x1,y1,x2,y2=after_section["rectangle"]
                    new_rectangle=(x1-2,y1-2,x1+1,y1+1)
                    new_section={"text":line,"rectangle":new_rectangle}
                    
                    self.results[page_index]["sections"][last_section_index]=new_section
                    
                    similarity_results = self.similarity_analayse.get_similarity_text_and_phrase_for_headers(clean_text(text=line,language=self.lang))
                    if len(similarity_results)!=0:
                        self.results[page_index]["bigger_sections"][last_section_index]=new_section
                        
                    last_section_index+=1

            # if similarity_results:
            #     self.results[page_index]['bigger_sections'][section_index] = {
            #         'text': lines,
            #         'similarity_results': similarity_results
            #     }
            # else:
            #     self.results[page_index]['sections'][lines] = {
            #         'text': section_text
            #     }
        self.lines=lines
        print()    
        
                
        # for page_index in range(len(self.results)):
        
        #     self.tesseract_result[page_index]["bigger_punkto"]=self.myDetectPunkto.detect_big_punkto(self.results[page_index]["punktos"])
        #     self.phrase_results=[]
        #     for section_index in self.results[page_index]["sections"]:
                
        #         text=self.results[page_index]["sections"][section_index]["text"]
        #         phrase_result_main=self.similarity_analayse.get_similarity_text_and_phrase_for_headers(clean_text(text=text,language=self.lang))
        #         if len(phrase_result)!=0:
        #             print("a")
                
        #         rectangle_text=self.results[page_index]["sections"][section_index]["rectangle_text"]
        #         phrase_result=self.similarity_analayse.get_similarity_text_and_phrase_for_headers(clean_text(text=rectangle_text,language=self.lang))
        #         if len(phrase_result)!=0:
        #             print("a")
                    
        #         phrase_result_rectangle=self.similarity_analayse.get_similarity_text_and_phrase_for_headers(clean_text(text=text,language=self.lang))
        #         # if len(phrase_result_main)!=0 or len(phrase_result_rectangle)!=0:
        #         #     self.results[page_index]["sections"][index]={"text":text, 
        #         #                                                 "phrase":phrase_result["phrase"],
        #         #                                                 "rectangle":(left,top,right,bottom)}
                        
        #         if punkto>=self.tesseract_result[page_index]["bigger_punkto"]:
        #             self.results[page_index]["bigger_sections"][index]= {"text":text, 
        #                                                                  "rectangle":(left,top,right,bottom)}
                                         

    def get_rectangles(self):
        
        rectangle_dict={}
        for page_index in self.results:
            
            max_width, max_height= self.pages[page_index].size
            
            for index in self.results[page_index]["bigger_sections"]:
                rectangle_dict[index]=self.results[page_index]["bigger_sections"][index]
                    
            my_rectangle_calculator=rectangle_calculator.RectangleCalculator(rectangle_dict,max_width,max_height)
            my_rectangle_calculator.find_rectangles()
                        
            for index in self.results[page_index]["bigger_sections"]:
                self.results[page_index]["bigger_sections"][index]=my_rectangle_calculator.sections[index]
            
    def rectangle_to_text(self):
        
        import shutil
        try:
            shutil.rmtree("crops")
        except:
            pass
        finally:
            os.makedirs("crops")
        
        for page_index in self.results:
            for index in self.results[page_index]["bigger_sections"]:
                self.results[page_index]["bigger_sections"][index]

                page=self.pages[page_index]
                text=self.results[page_index]["bigger_sections"][index]["text"]
                
                rectangle_image=page.crop(self.results[page_index]["bigger_sections"][index]["rectangle"])
                rectangle_1_image=page.crop(self.results[page_index]["bigger_sections"][index]["rectangle_1"])
                rectangle_2_image=page.crop(self.results[page_index]["bigger_sections"][index]["rectangle_2"])
                rectangle_3_image=page.crop(self.results[page_index]["bigger_sections"][index]["rectangle_3"])
                
                try:
                    rectangle_image.save(f"crops/{index}_rect.png")
                except:
                    pass
                try:
                    rectangle_1_image.save(f"crops/{index}_rect1.png")
                except:
                    pass
                try:
                    rectangle_2_image.save(f"crops/{index}_rect2.png")
                except:
                    pass
                try:
                    rectangle_3_image.save(f"crops/{index}_rect3.png")
                except:
                    pass
                
                # try:
                #     rectangle_image=page.crop(self.results[page_index]["bigger_sections"][index]["rectangle"])
                #     rectangle_image.save("rectangle_text.png")
                #     rectangle_1_image.save("rectangle_1_text.png")
                #     rectangle_2_image.save("rectangle_2_text.png")
                #     rectangle_3_image.save("rectangle_3_text.png")
                # except Exception as e:
                #     pass
                
                text1=""
                text2=""
                text3=""
                try:
                    text1 = " ".join(pytesseract.image_to_data(rectangle_1_image,output_type = pytesseract.Output.DICT, lang=self.lang)["text"])
                    self.results[page_index]["bigger_sections"][index]["rectangle_1_text"]=text1
                except:
                    pass
                try:
                    text2=" ".join(pytesseract.image_to_data(rectangle_2_image,output_type = pytesseract.Output.DICT, lang=self.lang)["text"])
                    self.results[page_index]["bigger_sections"][index]["rectangle_2_text"]=text2
                except:
                    pass
                try:
                    text3 =" ".join(pytesseract.image_to_data(rectangle_3_image,output_type = pytesseract.Output.DICT, lang=self.lang)["text"])
                    self.results[page_index]["bigger_sections"][index]["rectangle_3_text"]=text3
                except:
                    pass
                
                self.results[page_index]["bigger_sections"][index]["rectangle_text"]=f"{text1} {text2} {text3}"
                    
