from langdetect import detect

class LanguageDetect:
    def __init__(self) -> None:
        pass
    def detectLanguage(self,text):
        try:
            language= detect(text)
            if language=="en":
                return language
            return "tur"
        except Exception as e:
            return "en"
        

if __name__ == "__main__":
    myLanguageDetect=LanguageDetect()
    print(myLanguageDetect.detectLanguage("Merhaba, nasılsın"))
