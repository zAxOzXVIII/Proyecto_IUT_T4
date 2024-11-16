from rest_framework.decorators import api_view
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Estudiante, CustomUser
from .serializers import EstudianteSerializer
from .forms import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from django.conf import settings

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def estudiantesApi(request, id=0):
    if request.method == 'GET':
        estudiantes = Estudiante.objects.all()
        estudiantes_serializer = EstudianteSerializer(estudiantes, many=True)
        return Response(estudiantes_serializer.data)

    elif request.method == 'POST':
        estudiantes_serializer = EstudianteSerializer(data=request.data)
        if estudiantes_serializer.is_valid():
            estudiantes_serializer.save()
            return Response('Estudiante agregado', status=status.HTTP_201_CREATED)
        return Response(estudiantes_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        estudiante = Estudiante.objects.get(pk=id)
        estudiantes_serializer = EstudianteSerializer(estudiante, data=request.data)
        if estudiantes_serializer.is_valid():
            estudiantes_serializer.save()
            return Response('Estudiante actualizado')
        return Response(estudiantes_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        estudiante = Estudiante.objects.get(pk=id)
        estudiante.delete()
        return Response('Estudiante eliminado')


########################FUNCIONES CRUD##############################
def estudiantes_view(request):
    estudiantes = Estudiante.objects.all()
    estudiantes_eliminados = Estudiante.objects.filter(status__in=[False, False, 0])
    return render(request, 'estudiantes_main.html', {"estudiantes": estudiantes, "estudiantes_eliminados":estudiantes_eliminados, 'roles':request.session["staff_role"]})

def editar_estudiante(request, id):
    if request.method == "GET":
        estudiante = get_object_or_404(Estudiante, pk=id)
        form = EstudianteForm(instance=estudiante)
        #print(f"{estudiante.cedula}")
        #persuser = get_object_or_404(CustomUser, cedula=estudiante.cedula)
        #print(f"{persuser.email}")
        return render(request, "editar_estudiante.html", {"estudiante": estudiante, "form": form})
    elif request.method == "POST":
        try:
            estudiante = get_object_or_404(Estudiante, pk=id)
            form = EstudianteForm(request.POST, instance=estudiante)
            form.save()
            #print(f"{estudiante.cedula}") ###
            messages.success(request, 'Estudiante actualizado exitosamente.')
            return redirect("estudiantes_main")
        except ValueError:
            return render(request, "editar_estudiante.html", {"estudiante": estudiante, "form": form, "error": "Error updating estudiante"})
###
def activar_estudiante(request, id):
    if request.method == "POST":
        estudiante = get_object_or_404(Estudiante, pk=id)
        #print(estudiante.nombre)
        estudiante.status = True
        estudiante.save()
        messages.success(request, 'Estudiante activado exitosamente.')
        return redirect('estudiantes_main')
###

def eliminar_estudiante(request, id):
    if request.method == "GET":
        estudiante = get_object_or_404(Estudiante, pk=id)
        #print(f"{estudiante.cedula}")
        return render(request, 'eliminar_estudiante.html', {"estudiante": estudiante})
    elif request.method == "POST":
        estudiante = get_object_or_404(Estudiante, pk=id)
        estudiante.status = False
        estudiante.save()
        messages.success(request, 'Estudiante eliminado exitosamente.')
        return redirect('estudiantes_main')

def estudiantes_eliminados(request):
    # Filtrar profesores que tienen status=False (inactivos)
    estudiantes_inactivos = Estudiante.objects.all()
    # Renderizar el template y pasar los profesores inactivos al contexto
    return render(request, 'estudiantes_eliminados.html', {'estudiantes_inactivos': estudiantes_inactivos})

def generar_pdf_estudiantes(request):
    # Crear un objeto HttpResponse con el tipo de contenido adecuado para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="estudiantes.pdf"'

    # Crear el objeto Canvas
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    pdf.setTitle("Listado de Estudiantes")

    # Ruta de la imagen (asegúrate de que la ruta sea correcta)
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo_iut_largo.jpg')
    logo_path = logo_path.replace('\\', '/')

    # Agregar la imagen en el encabezado (ajusta el tamaño y posición según sea necesario)
    pdf.drawImage(logo_path, 40, height - 100, width=200, height=60)  # Ajusta la posición y el tamaño de la imagen

    # Margen superior (debajo de la imagen)
    y = height - 150

    # Escribir el título debajo de la imagen
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, y, "Lista de Estudiantes")
    y -= 30

    # Definir estilo para el contenido
    pdf.setFont("Helvetica", 12)

    # Iterar sobre los estudiantes y escribir la información en el PDF
    estudiantes = Estudiante.objects.all()
    for estudiante in estudiantes:
        if y < 100:  # Si el espacio no es suficiente, crear una nueva página
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = height - 50

        pdf.drawString(100, y, f"Nombre: {estudiante.nombre} {estudiante.apellido}")
        y -= 20
        pdf.drawString(100, y, f"Cédula: {estudiante.cedula}")
        y -= 20
        pdf.drawString(100, y, f"Email: {estudiante.email}")
        y -= 20
        pdf.drawString(100, y, f"Sección: {estudiante.seccion}")
        y -= 20
        pdf.drawString(100, y, f"Fecha de Nacimiento: {estudiante.fecha_nacimiento}")
        y -= 20
        pdf.drawString(100, y, f"Teléfono: {estudiante.numero_telefono}")
        y -= 20
        pdf.drawString(100, y, f"Dirección: {estudiante.direccion}")
        y -= 20
        pdf.drawString(100, y, f"Sexo: {estudiante.sexo}")
        y -= 20
        pdf.drawString(100, y, f"Status: {'Activo' if estudiante.status else 'Inactivo'}")
        y -= 40  # Espacio adicional entre estudiantes

    # Finalizar el PDF
    pdf.showPage()
    pdf.save()

    return response

def buscar_estudiante(request):
    estudiante = None
    form = BuscarEstudianteForm()

    if request.method == 'POST':
        form = BuscarEstudianteForm(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            try:
                # Realiza la búsqueda de estudiante por cédula
                estudiante = get_object_or_404(Estudiante, cedula=cedula)
            except Exception as e:
                # Manejar cualquier otra excepción que pueda ocurrir
                messages.error(request, f'Ocurrió un error: No se encontró un estudiante con esa cédula.')

    return render(request, 'buscar_estudiante.html', {'form': form, 'estudiante': estudiante})

def dashboard(request):
    estudiantes = Estudiante.objects.all()  # Obtener todos los estudiantes
    return render(request, 'dashboard.html', {'estudiantes': estudiantes})