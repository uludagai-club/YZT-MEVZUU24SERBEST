import json
from sentence_transformers import SentenceTransformer, util
import Levenshtein


class Similarity_Analayse:
    def __init__(self,min_score) -> None:
        self.min_score=min_score
        self.models={"tr":SentenceTransformer('emrecan/bert-base-turkish-cased-mean-nli-stsb-tr'),
                     "en":SentenceTransformer('paraphrase-xlm-r-multilingual-v1')}

        self.pharse_json=json.load(open("utils/parser_phrases.json", encoding="utf-8"))


    def get_similarity_text_and_phrase_for_headers(self,text):
        
        result_list=[]
        for item in self.pharse_json:
            for key, value in item.items():
                for phrase in value["phrases"].split(","):
                    distance=Levenshtein.distance(text, phrase)
                    similarity =1 -(distance / max(len(text), len(phrase)))
                    if similarity>=self.min_score:
                        result_list.append({"phrase":key,"score":similarity,"text":text})
        return result_list

    def get_similarity(self,language,text_1,text_2):
        model= self.models[language]
        text_1_embedding = model.encode(text_1, convert_to_tensor=True)
        text_2_embedding = model.encode(text_2, convert_to_tensor=True)
        similarity=util.pytorch_cos_sim(text_1_embedding, text_2_embedding)
        result=similarity.item()

    
    
if __name__=="__main__":
    my_similarity_analayse=Similarity_Analayse(0.85)
    my_similarity_analayse.get_similarity("tr","EGITIM","EGITIM")