from django.shortcuts import render, redirect
from .forms import (
    CVForm
)
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from utils.evaluate_resumes import evaluate_resumes
from utils.compare_specs import compare_specs
from django.http import JsonResponse


def evaluation(request):
    if request.method == 'POST':
        form = CVForm(request.POST, request.FILES)

        if form.is_valid():
            
            education = form.cleaned_data['education']
            education_score = form.cleaned_data['education_score']
            soft_skill = form.cleaned_data['soft_skill']
            soft_skill_score = form.cleaned_data['soft_skill_score']
            hard_skill = form.cleaned_data['hard_skill']
            hard_skill_score = form.cleaned_data['hard_skill_score']
            languages = form.cleaned_data['languages']
            languages_score = form.cleaned_data['languages_score']
            driver_license = form.cleaned_data['driver_license']
            driver_license_point = form.cleaned_data['driver_license_point']
            files = request.FILES.getlist('files')

            compare_list={
                "Education":education.split(","),
                "Education Score":education_score,
                "Soft Skill":soft_skill.split(","),
                "Soft Skill Score":soft_skill_score,
                "Hard Skill":hard_skill.split(","),
                "Hard Skill Score":hard_skill_score,
                "Languages":languages.split(","),
                "Languages Score": languages_score,
                "Driver License":driver_license.split(","),
                "Driver License Score":driver_license_point,
            }

            # Dosyaları kaydet
            fs = FileSystemStorage()
            file_paths=[]
            for file in files:
                # Zaman damgası ile dosya adını oluştur
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{timestamp}_{file.name}"
                fs.save(file_name, file)
                file_path=f"{fs.location}/{file_name}"
                file_paths.append(file_path)

            evaluated_resumes=evaluate_resumes(file_paths)
            compared_specs=compare_specs(evaluated_resumes,compare_list)
            return JsonResponse({"compared_specs":compared_specs,"resume_results":evaluated_resumes})

            
    else:
        
        return render(request, 'evaluation.html', {})



