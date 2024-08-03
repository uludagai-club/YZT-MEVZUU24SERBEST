from django.urls import path
from . import views

# http://127.0.0.1:8000/home
# http://127.0.0.1:8000/loading
# http://127.0.0.1:8000/evaluation

urlpatterns = [
    path("", views.loading, name='loading'),
    path("loading/", views.loading, name='loading'),
    path("loading/loading.html", views.loading, name='loading'),
    path("loading.html", views.loading, name='loading')
]