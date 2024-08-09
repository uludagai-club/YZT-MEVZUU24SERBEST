from main import Tesseract_Operator 

def evaluate_resumes(file_paths):
    results={}
    for file_path in file_paths:

        operator=Tesseract_Operator(file_path=file_path)
        operator.do_tesseract_parts()
        operator.get_contact_infos()

        context=[]
        
        for page_number in operator.tesseract.results:
            if type(page_number)==int:
                for bigger_section_number in operator.tesseract.results[page_number]["bigger_sections"]:
                    value=operator.tesseract.results[page_number]["bigger_sections"][bigger_section_number]
                    main_text=value["text"]
                    try:
                        rectangle_1_text=value["rectangle_1_text"]
                    except:
                        rectangle_1_text=""
                    try:
                        rectangle_2_text=value["rectangle_2_text"]
                    except:
                        rectangle_2_text=""
                    try:
                        rectangle_3_text=value["rectangle_3_text"]
                    except:
                        rectangle_3_text=""
                        
                    phrase=value["phrase"]
        
                    context.append({
                        "text":main_text+"\n"+
                        rectangle_1_text+"\n"+
                        rectangle_2_text+"\n"+
                        rectangle_3_text,
                        "phrase":phrase,"score":None})
            else:
                emails=operator.tesseract.results["emails"]
                domains=operator.tesseract.results["domains"]
                phones=operator.tesseract.results["phones"]
                universities=operator.tesseract.results["universities"]
                
                for email in emails:
                    context.append({
                        "text":email,
                        "phrase":"email","score":None})
                    
                for domain in domains:
                    context.append({
                        "text":domain,
                        "phrase":"domain","score":None})
                
                for phone in phones:
                    context.append({
                        "text":phone,
                        "phrase":"phone","score":None})
                    
                for university_item in universities:
                    context.append({
                        "text":university_item["University"],
                        "phrase":"university","score":university_item["Global Score"]})
                    
        results[file_path]=context

    return results