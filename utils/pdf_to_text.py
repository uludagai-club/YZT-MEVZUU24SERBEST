import PyPDF2

def pdf_to_text(pdf_file_path):
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text()
    return text_content