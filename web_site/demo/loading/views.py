from django.shortcuts import render

def loading(request):
    return render(request, "loading.html")
