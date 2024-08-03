import os
from uuid import uuid4

def savePdf(instance, filename):
    unique_id = uuid4().hex[:10]
    filename = f'{unique_id}.pdf'
    return os.path.join('documents', filename)

"""def handle_uploaded_file(f):
    upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media', 'documents')
    unique_id = uuid4().hex[:10]
    filename = f'{unique_id}.pdf'
    file_path = os.path.join(upload_dir, filename) 

    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path"""

def handle_uploaded_file(f):
    upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media', 'documents')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    file_path = os.path.join(upload_dir, f.name) 

    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    return file_path
