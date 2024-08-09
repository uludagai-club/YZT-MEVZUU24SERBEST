from django.urls import path
from . import views

# http://127.0.0.1:8000/home
# http://127.0.0.1:8000/loading
# http://127.0.0.1:8000/evaluation

urlpatterns = [
    path("", views.home, name='home'),
    path("home/", views.home, name='home'),
    path('save_pdfs/', views.save_uploaded_pdfs, name='save_pdfs'),
    path("home/home.html", views.home, name='home'),
    path('upload/', views.upload_file, name='upload_file')
]   