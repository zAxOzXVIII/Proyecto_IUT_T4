from django.shortcuts import render, get_object_or_404, redirect
from .models import ArchivosEstudiantes
from grupos.models import Grupos
from .forms import ArchivoEstudianteForm
from django.contrib import messages
from accounts.models import Estudiante

# Create your views here.
def proyectos_home(request):
    return render(request, 'home_proyectos.html')

def subir_archivo(request):
    user_id = request.session.get('user_id')  # ID del estudiante logueado
    print(user_id)
# Obtener todos los grupos
    grupos = Grupos.objects.all()

# Validar si el ID del usuario está en el listado de estudiantes de algún grupo
    grupo_usuario = None
    for grupo in grupos:
        estudiantes_ids = grupo.get_estudiantes()  # Devuelve la lista de IDs de estudiantes como ['1', '2', '3', '4']
        if str(user_id) in estudiantes_ids:
            grupo_usuario = grupo
            break

    if grupo_usuario:
        print(f"El usuario pertenece al grupo: {grupo_usuario}")
    else:
        print("El usuario no pertenece a ningún grupo.")

    if not grupo:
        messages.error(request, "No estás asociado a ningún grupo.")
        return redirect('listar_archivos')

    archivo_existente = ArchivosEstudiantes.objects.filter(Grupo_est_id=grupo.id).first()

    if archivo_existente:
        # Si ya hay un archivo subido en el grupo, validar si fue subido por el usuario actual
        if str(user_id) in grupo.get_estudiantes() and archivo_existente.Grupo_est_id == grupo.id:
            messages.error(request, "Ya subiste un archivo. Solo puedes actualizarlo o eliminarlo.")
            return redirect('listar_archivos')

    if request.method == 'POST':
        form = ArchivoEstudianteForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.Grupo_est_id = grupo.id  # Asignar el grupo al archivo
            if grupo_usuario:
                print(grupo.id)
                messages.success(request, "Archivo subido exitosamente.")
            else: messages.success(request, "No esta en ningun grupo")
            return redirect('listar_archivos')
    else:
        form = ArchivoEstudianteForm()

    return render(request, 'archivos/subir_archivo.html', {'form': form})

def listar_archivos(request):
    user_id = request.session.get('user_id')
    grupo = Grupos.objects.filter(estudiantes__icontains=str(user_id)).first()
    archivos = ArchivosEstudiantes.objects.filter(Grupo_est_id=grupo.id) if grupo else []

    return render(request, 'archivos/listar_archivos.html', {'archivos': archivos, 'grupo': grupo, 'user_id': user_id})

def listar_archivos_all(request):
    # Obtener todos los archivos
    archivos = ArchivosEstudiantes.objects.all()

    # Crear un diccionario para almacenar los estudiantes relacionados con cada grupo
    estudiantes_info = []

    # Iterar sobre los grupos y obtener los estudiantes
    grupos = Grupos.objects.all()
    for grupo in grupos:
        if grupo.estudiantes:  # Si el grupo tiene estudiantes asignados
            # Separar los IDs y convertirlos en una lista
            estudiantes_ids = [int(id.strip()) for id in grupo.estudiantes.split(',') if id.strip().isdigit()]
            
            # Obtener los estudiantes de la base de datos
            estudiantes = Estudiante.objects.filter(id__in=estudiantes_ids)

            # Agregar la información al diccionario con el ID del grupo
            estudiantes_info.append({
                'id_grupo': grupo.id,
                'estudiantes': [
                    {'nombre': estudiante.nombre, 'cedula': estudiante.cedula}
                    for estudiante in estudiantes
                ]
            })

    # Pasar los datos al contexto
    return render(request, 'archivos/listar_archivos_staff.html', {
        'archivos': archivos,
        'grupos': estudiantes_info
    })

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
