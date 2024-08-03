from django.http import HttpResponseRedirect
from django.shortcuts import render
from home.forms import UploadFileForm
from home.utils import handle_uploaded_file
import uuid
import os,sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
up_parent_dir = os.path.dirname(parent_dir)
up2_parent_dir = os.path.dirname(up_parent_dir)
sys.path.append(parent_dir)
sys.path.append(up_parent_dir)
sys.path.append(up2_parent_dir)

from main import Operator

def home(request):
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Form geçerliyse, dosya yükleme işlemini gerçekleştirin
            file = request.FILES['file']
            file_path=upload_file(file)
            do_extract(file_path=file_path)
            
            context={"University":"aaaaaa",
                    "asdasdasd":"vdbfdgbfgbfg",
                    "Eti":"Django"}
            

    else:
        form = UploadFileForm()
        context = {
            'form': form,
        }
    return render(request, "home.html",context)

def save_uploaded_pdfs(request):
    return render(request, "save_pdfs")

def upload_file(file):
    import os
    
    new_filename = str(uuid.uuid4()) + os.path.splitext(file.name)[1]
    file_path = os.path.join('web_site','demo','media', new_filename)
    
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path


def do_extract(file_path):
    operator=Operator(file_path=file_path)
    operator.do_tesseract_parts()
    operator.get_contact_infos()
    