from django import forms
from .models import File


class CVForm(forms.ModelForm):
    education = forms.CharField(max_length=200, required=False)
    education_score = forms.IntegerField(min_value=0, max_value=100, required=False)
    soft_skill = forms.CharField(max_length=200, required=False)
    soft_skill_score = forms.IntegerField(min_value=0, max_value=100, required=False)
    hard_skill = forms.CharField(max_length=200, required=False)
    hard_skill_score = forms.IntegerField(min_value=0, max_value=100, required=False)
    languages = forms.CharField(max_length=200, required=False)
    languages_score = forms.IntegerField(min_value=0, max_value=100, required=False)
    driver_license = forms.CharField(max_length=100, required=False)
    driver_license_point = forms.IntegerField(min_value=0, max_value=100, required=False)
    files = forms.FileField()

    class Meta:
        model = File
        fields = ('files', )