from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
#from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profesores
from .forms import ProfesoresForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Create your views here.

def profesores_view(request):
    profes = Profesores.objects.all()
    ### filtra si hay profesores con status False
    profes_eliminados = Profesores.objects.filter(status__in=[False, False, 0])
    return render(request, 'profesores_main.html', {"profes": profes, "profes_eliminados":profes_eliminados, "roles":request.session["staff_role"]})

def crear_profe(request):
    if request.method == "GET":
        return render(request, 'crear_profe.html', {"form": ProfesoresForm()})
    else:
        try:
            form = ProfesoresForm(request.POST)
            if form.is_valid():
                form.save()
                print("Profesor guardado")
                return redirect("profesores")
            else:
                # Si el formulario no es válido, renderiza la misma página con el formulario y los errores
                return render(request, 'crear_profe.html', {"form": form, "error": "Formulario inválido"})
        except Exception as e:
            # Capturar el error y mostrar mensaje en el template
            return render(request, 'crear_profe.html', {"form": ProfesoresForm(), "error": str(e)})

def editar_profe(request, id):
    if request.method == "GET":
        profe = get_object_or_404(Profesores, pk=id)
        form = ProfesoresForm(instance=profe)
        return render(request, "editar_profe.html", {"profe": profe, "form": form})
    else:
        try:
            profe = get_object_or_404(Profesores, pk=id)
            form = ProfesoresForm(request.POST, instance=profe)
            form.save()
            messages.success(request, 'Profe actualizado exitosamente.')
            return redirect("profesores")
        except ValueError:
            return render(request, "editar_profe.html", {"profe": profe, "form": form, "error": "Error updating Prof"})

def activar_profe(request,id):
    if request.method == "POST":
        profe = get_object_or_404(Profesores, pk=id)
        print(profe.nombre)
        profe.status = True
        profe.save()
        messages.success(request, 'Profesor activado exitosamente.')
        return redirect('profesores')

def eliminar_profe(request, id):
    if request.method == "GET":
        profe = get_object_or_404(Profesores, pk=id)
        return render(request, 'eliminar_profe.html', {"profe": profe})
    if request.method == "POST":
        profe = get_object_or_404(Profesores, pk=id)
        profe.status = False
        profe.save()
        messages.success(request, 'Profesor eliminado exitosamente.')
        return redirect('profesores')


def profesores_eliminados(request):
    # Filtrar profesores que tienen status=False (inactivos)
    profes_inactivos = Profesores.objects.all()
    # Renderizar el template y pasar los profesores inactivos al contexto
    return render(request, 'profesores_eliminados.html', {'profes_inactivos': profes_inactivos})

def generar_pdf_profesores(request):
    # Crear un objeto HttpResponse con el tipo de contenido adecuado para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="profesores.pdf"'

    # Crear el objeto Canvas
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    pdf.setTitle("Listado de Profesores")

    # Margen superior
    y = height - 50

    # Escribir encabezado
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, y, "Lista de Profesores")
    y -= 30

    # Definir estilo para el contenido
    pdf.setFont("Helvetica", 12)

    # Iterar sobre los profesores y escribir la información en el PDF
    profesores = Profesores.objects.all()
    for profesor in profesores:
        if y < 100:  # Si el espacio no es suficiente, crear una nueva página
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = height - 50

        pdf.drawString(100, y, f"Nombre: {profesor.nombre} {profesor.apellido}")
        y -= 20
        pdf.drawString(100, y, f"Cédula: {profesor.cedula}")
        y -= 20
        pdf.drawString(100, y, f"Correo: {profesor.correo}")
        y -= 20
        pdf.drawString(100, y, f"Rol: {profesor.role}")
        y -= 20
        pdf.drawString(100, y, f"Status: {'Activo' if profesor.status else 'Inactivo'}")
        y -= 40  # Espacio adicional entre profesores

    # Finalizar el PDF
    pdf.showPage()
    pdf.save()

    return response