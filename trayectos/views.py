from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Estudiante
from trayectos.models import Trayectos_all
from django.contrib import messages
from .forms import AsignarEstudiantesForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
from django.conf import settings

def trayectos_main(request):
    if request.method == "GET":
        return render(request, "trayectos_main.html")

def trayectos_view(request):
    if request.method == "GET":
        return render(request, "trayectos_view.html")

    elif request.method == "POST":
        trayectos = request.POST.get('trayecto')
        seccion = request.POST.get('seccion')
        if seccion == "":
            seccion = "all"

        if trayectos:
            tray = trayectos # pasar el str
        if not trayectos:
            return render(request, "trayectos_view.html", {"error": "debe seleccionar un trayecto para visualizar"})

        if trayectos == "1":
            estudiantes = Trayectos_all.objects.filter(trayecto_año="1")
            print(estudiantes)
        if trayectos == "2":
            estudiantes = Trayectos_all.objects.filter(trayecto_año="2")
            print(estudiantes)
        if trayectos == "3":
            estudiantes = Trayectos_all.objects.filter(trayecto_año="3")
            print(estudiantes)
        if trayectos == "4":
            estudiantes = Trayectos_all.objects.filter(trayecto_año="4")
            print(estudiantes)
        print(request.session["staff_role"])
        return render(request, "trayectos_view.html", {"estudiantes": estudiantes, "seccion": seccion, "trayecto": tray, "roles":request.session["staff_role"]})

def asignar_estudiantes(request):
    if request.method == 'POST':
        form = AsignarEstudiantesForm(request.POST)
        if form.is_valid():
            estudiantes = form.cleaned_data['estudiantes']
            cedulas = estudiantes.values('cedula')
            nombres = estudiantes.values('nombre')
            seccion = form.cleaned_data['seccion']
            trayectos = request.POST.get('trayecto')
            
            
            if trayectos == "":
                messages.success(request, "debe seleccionar un trayecto")
                return redirect('asignar_estudiantes')
            x = 0
            # Asignar a los trayectos seleccionados
            for estudiante in estudiantes:
                if not Trayectos_all.objects.filter(ref_cedula=estudiante):
                    #si no coincide en nada, guardamos
                    Trayectos_all.objects.create(ref_cedula=estudiante, ci_est=estudiante.cedula, name_est=estudiante.nombre , seccion=seccion, trayecto_año=trayectos, codigo_año=f"SID{trayectos}{seccion}")
                    x = 1 #verificar si se añadio algo
                else:
                    estudiante_existente = Trayectos_all.objects.get(ref_cedula=estudiante)
                    print(estudiante_existente.trayecto_año)
                    messages.success(request, f"estudiante {estudiante.nombre} ya esta registrado en Trayecto {estudiante_existente.trayecto_año}")
                    continue
            if x >= 1:
                messages.success(request, 'estudiantes agregados correctamente.')
            return redirect('asignar_estudiantes')
        else:
            # Mostrar errores del formulario
            messages.error(request, 'Error en el formulario. Por favor revise los campos')
    elif request.method == "GET":
        form = AsignarEstudiantesForm()
    estudiantes = Estudiante.objects.all()
    return render(request, 'registrar_trayectos.html', {'form': form, 'estudiantes': estudiantes})



def trayectos_edit(request, tr, id):
    if request.method == "GET":
        est = get_object_or_404(Trayectos_all, ref_cedula_id=id) #estudiante
        return render(request, "trayectos_edit.html", {"estudiante": est, "trayecto": tr})

    elif request.method == "POST":
        trayecto_new = request.POST.get('trayecto')
        seccion_new = request.POST.get('seccion')
        if trayecto_new == "": trayecto_new = tr
        if seccion_new == "": seccion_new = Trayectos_all.objects.get(ref_cedula_id=id).seccion
        codigo_new = f"SID{trayecto_new}{seccion_new}"

        Trayectos_all.objects.filter(ref_cedula_id=id).update(trayecto_año=trayecto_new)
        Trayectos_all.objects.filter(ref_cedula_id=id).update(seccion=seccion_new)
        Trayectos_all.objects.filter(ref_cedula_id=id).update(codigo_año=codigo_new)
        messages.success(request, 'Estudiante actualizado.')
        return redirect("trayectos_view")

def trayectos_delete(request, tr, id):
        if request.method == "GET":
        #tr alamcena que trayecto se maneja
            est = get_object_or_404(Trayectos_all, ref_cedula_id=id)
            return render(request, "trayectos_delete.html", {"estudiante": est, "trayecto": tr})

        elif request.method == "POST":
            Trayectos_all.objects.filter(ref_cedula_id=id).delete()
            messages.success(request, f'Estudiante eliminado de {tr}.')
        return redirect("trayectos_view")

################################################################################
################################################################################
# pdf de trayectos
def generar_pdf_trayecto1(request):
    # Crear un objeto HttpResponse con el tipo de contenido adecuado para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="trayectos.pdf"'

    # Crear el objeto Canvas
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    pdf.setTitle("Listado de Estudiantes por Trayecto")

    # Configurar márgenes
    margen_x = 50
    margen_y = 50
    contenido_ancho = width - 2 * margen_x
    contenido_alto = height - 2 * margen_y

    # Añadir una imagen de encabezado
    imagen_ruta = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo_iut_largo.jpg')  # Cambia esta ruta por la de tu imagen
    imagen_ancho = 500  # Ajusta el ancho según sea necesario
    imagen_alto = 50  # Ajusta el alto según sea necesario
    pdf.drawImage(ImageReader(imagen_ruta), margen_x, height - margen_y - imagen_alto, width=imagen_ancho, height=imagen_alto)

    # Margen superior ajustado para el contenido
    y = height - margen_y - imagen_alto - 20

    # Función para escribir el título de cada trayecto
    def escribir_trayecto(titulo, y_pos):
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(margen_x, y_pos, titulo)
        pdf.setFont("Helvetica", 12)
        return y_pos - 20

    # Función para escribir los datos de los estudiantes
    def escribir_estudiante(y_pos, estudiante):
        pdf.drawString(margen_x, y_pos, f"Cédula: {estudiante.ci_est}, Nombre: {estudiante.name_est}, Sección: {estudiante.seccion}")
        return y_pos - 20

    # Escribir datos de Trayecto 1
    y = escribir_trayecto("Trayecto 1", y)
    for estudiante in Trayectos_all.objects.filter(trayecto_año=1):
        # Comprobar si hay espacio suficiente en la página
        if y < margen_y:
            pdf.showPage()
            y = height - margen_y
        y = escribir_estudiante(y, estudiante)

    # Finalizar el PDF
    pdf.showPage()
    pdf.save()

    return response

def generar_pdf_trayecto2(request):
    # Crear un objeto HttpResponse con el tipo de contenido adecuado para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="trayectos.pdf"'

    # Crear el objeto Canvas
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    pdf.setTitle("Listado de Estudiantes por Trayecto")

    # Configurar márgenes
    margen_x = 50
    margen_y = 50
    contenido_ancho = width - 2 * margen_x
    contenido_alto = height - 2 * margen_y

    # Añadir una imagen de encabezado
    imagen_ruta = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo_iut_largo.jpg')  # Cambia esta ruta por la de tu imagen
    imagen_ancho = 500  # Ajusta el ancho según sea necesario
    imagen_alto = 50  # Ajusta el alto según sea necesario
    pdf.drawImage(ImageReader(imagen_ruta), margen_x, height - margen_y - imagen_alto, width=imagen_ancho, height=imagen_alto)

    # Margen superior ajustado para el contenido
    y = height - margen_y - imagen_alto - 20

    # Función para escribir el título de cada trayecto
    def escribir_trayecto(titulo, y_pos):
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(margen_x, y_pos, titulo)
        pdf.setFont("Helvetica", 12)
        return y_pos - 20

    # Función para escribir los datos de los estudiantes
    def escribir_estudiante(y_pos, estudiante):
        pdf.drawString(margen_x, y_pos, f"Cédula: {estudiante.ci_est}, Nombre: {estudiante.name_est}, Sección: {estudiante.seccion}")
        return y_pos - 20

    # Escribir datos de Trayecto 2
    y = escribir_trayecto("Trayecto 2", y)
    for estudiante in Trayectos_all.objects.filter(trayecto_año=2):
        # Comprobar si hay espacio suficiente en la página
        if y < margen_y:
            pdf.showPage()
            # Redibujar encabezado e imagen en la nueva página
            pdf.drawImage(ImageReader(imagen_ruta), margen_x, height - margen_y - imagen_alto, width=imagen_ancho, height=imagen_alto)
            y = height - margen_y - imagen_alto - 20
            y = escribir_trayecto("Trayecto 2", y)
        y = escribir_estudiante(y, estudiante)

    # Finalizar el PDF
    pdf.showPage()
    pdf.save()

    return response

def generar_pdf_trayecto3(request):
    # Crear un objeto HttpResponse con el tipo de contenido adecuado para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="trayectos_trayecto3.pdf"'

    # Crear el objeto Canvas
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    pdf.setTitle("Listado de Estudiantes por Trayecto")

    # Configurar márgenes
    margen_x = 50
    margen_y = 50
    contenido_ancho = width - 2 * margen_x
    contenido_alto = height - 2 * margen_y

    # Añadir una imagen de encabezado
    imagen_ruta = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo_iut_largo.jpg')  # Cambia esta ruta por la de tu imagen
    imagen_ancho = 500  # Ajusta el ancho según sea necesario
    imagen_alto = 50  # Ajusta el alto según sea necesario
    pdf.drawImage(ImageReader(imagen_ruta), margen_x, height - margen_y - imagen_alto, width=imagen_ancho, height=imagen_alto)

    # Margen superior ajustado para el contenido
    y = height - margen_y - imagen_alto - 20

    # Función para escribir el título de cada trayecto
    def escribir_trayecto(titulo, y_pos):
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(margen_x, y_pos, titulo)
        pdf.setFont("Helvetica", 12)
        return y_pos - 20

    # Función para escribir los datos de los estudiantes
    def escribir_estudiante(y_pos, estudiante):
        pdf.drawString(margen_x, y_pos, f"Cédula: {estudiante.ci_est}, Nombre: {estudiante.name_est}, Sección: {estudiante.seccion}")
        return y_pos - 20

    # Escribir datos de Trayecto 3
    y = escribir_trayecto("Trayecto 3", y)
    for estudiante in Trayectos_all.objects.filter(trayecto_año=3):
        # Comprobar si hay espacio suficiente en la página
        if y < margen_y:
            pdf.showPage()
            # Redibujar encabezado e imagen en la nueva página
            pdf.drawImage(ImageReader(imagen_ruta), margen_x, height - margen_y - imagen_alto, width=imagen_ancho, height=imagen_alto)
            y = height - margen_y - imagen_alto - 20
            y = escribir_trayecto("Trayecto 3", y)
        y = escribir_estudiante(y, estudiante)

    # Finalizar el PDF
    pdf.showPage()
    pdf.save()

    return response

def generar_pdf_trayecto4(request):
    # Crear un objeto HttpResponse con el tipo de contenido adecuado para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="trayectos.pdf"'

    # Crear el objeto Canvas
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    pdf.setTitle("Listado de Estudiantes por Trayecto")

    # Margen superior
    y = height - 50

    # Función para escribir el título de cada trayecto
    def escribir_trayecto(titulo, y_pos):
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(100, y_pos, titulo)
        pdf.setFont("Helvetica", 12)
        return y_pos - 20

    # Función para escribir los datos de los estudiantes
    def escribir_estudiante(y_pos, estudiante):
        pdf.drawString(100, y_pos, f"Cédula: {estudiante.ci_est}, Nombre: {estudiante.name_est}, Sección: {estudiante.seccion}")
        return y_pos - 20

    # Escribir datos de Trayecto 4
    y = escribir_trayecto("Trayecto 4", y)
    for estudiante in Trayectos_all.objects.filter(trayecto_año=4):
        y = escribir_estudiante(y, estudiante)

    # Finalizar el PDF
    pdf.showPage()
    pdf.save()

    return response