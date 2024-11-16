from django.urls import path
from . import views

urlpatterns = [
    path('profesores/', views.profesores_view, name='profesores'),
    path('crear_profe/', views.crear_profe, name='crear_profe'),
    path('editar_profe/<int:id>/', views.editar_profe, name='editar_profe'),
    path('eliminar_profe/<int:id>/', views.eliminar_profe, name="eliminar_profe"),
    path('activar_profe/<int:id>/', views.activar_profe, name='activar_profe'),
    path('profesores/inactivos/', views.profesores_eliminados, name="profesores_eliminados"),
    path('generar_pdf_profesores/', views.generar_pdf_profesores, name='generar_pdf_profesores'),
]