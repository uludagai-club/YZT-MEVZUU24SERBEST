import json
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
import torch

class Ner:
    
    def __init__(self,language) -> None:
        self.getSources()
        self.language=language
        self.modelInitiate()
    
    def modelInitiate(self):
        self.model = AutoModelForTokenClassification.from_pretrained(self.nerSources[self.language]["Model"])
        self.tokenizer = AutoTokenizer.from_pretrained(self.nerSources[self.language]["Tokenizer"])
        self.ner=pipeline('ner', model=self.model, tokenizer=self.tokenizer)

    def getNer(self,text,demandedSections=[]):
        nerResult = self.ner(text)
        filtered_entities={}
        for item in nerResult:
            if item['entity'] in demandedSections:
                entity_type = item['entity']
                word = item['word']
                index=item["index"]
                if entity_type not in filtered_entities:
                    filtered_entities[entity_type] = []
                filtered_entities[entity_type].append({"word":word,"index":index})

        return filtered_entities
    
    def getSources(self):
        with open("utils/nerSources.json", "r", encoding="utf-8") as file:
            self.nerSources = json.load(file)

if __name__ == "__main__":
    myner=Ner("tr")
    result=myner.getNer("Mustafa Kemal Atatürk 19 Mayıs 1919'da Samsun'a ayak bastı.",["B-PER","I-PER"])
    print(result)
