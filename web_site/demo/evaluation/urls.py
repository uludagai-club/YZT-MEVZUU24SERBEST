from django.urls import path
from . import views

# http://127.0.0.1:8000/evaluation
# http://127.0.0.1:8000/evaluation

urlpatterns = [
    path("", views.evaluation, name='evaluation'),
    path("evaluation/", views.evaluation, name='evaluation')
]