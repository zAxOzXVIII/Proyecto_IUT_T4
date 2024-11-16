from django.shortcuts import render

# Create your views here.
def proyectos_home(request):
    return render(request, 'home_proyectos.html')