from django.shortcuts import render, get_object_or_404, redirect
from .models import ArchivosEstudiantes
from grupos.models import Grupos
from .forms import ArchivoEstudianteForm
from django.contrib import messages

# Create your views here.
def proyectos_home(request):
    return render(request, 'home_proyectos.html')

def subir_archivo(request):
    if request.method == 'POST':
        form = ArchivoEstudianteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Archivo subido exitosamente.")
            return redirect('listar_archivos')
    else:
        form = ArchivoEstudianteForm()
    return render(request, 'archivos/subir_archivo.html', {'form': form})

def listar_archivos(request):
    archivos = ArchivosEstudiantes.objects.all()
    return render(request, 'archivos/listar_archivos.html', {'archivos': archivos})

def editar_archivo(request, archivo_id):
    archivo = get_object_or_404(ArchivosEstudiantes, id=archivo_id)
    if request.method == 'POST':
        form = ArchivoEstudianteForm(request.POST, request.FILES, instance=archivo)
        if form.is_valid():
            form.save()
            messages.success(request, "Archivo actualizado exitosamente.")
            return redirect('listar_archivos')
    else:
        form = ArchivoEstudianteForm(instance=archivo)
    return render(request, 'archivos/editar_archivo.html', {'form': form})

def eliminar_archivo(request, archivo_id):
    archivo = get_object_or_404(ArchivosEstudiantes, id=archivo_id)
    if request.method == 'POST':
        archivo.delete()
        messages.success(request, "Archivo eliminado exitosamente.")
        return redirect('listar_archivos')
    return render(request, 'archivos/eliminar_archivo.html', {'archivo': archivo})
