from django.urls import path, include
from . import views
from masters import urls

urlpatterns = [
    path('', views.proyectos_home, name='home_pp'),
]
