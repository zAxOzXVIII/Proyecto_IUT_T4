from django import forms
from .models import ArchivosEstudiantes

class ArchivoEstudianteForm(forms.ModelForm):
    class Meta:
        model = ArchivosEstudiantes
        fields = ['Proyecto', 'Capitulos', 'Grupo_est_id']

    def clean_Proyecto(self):
        proyecto = self.cleaned_data.get('Proyecto')
        if not proyecto.name.endswith('.rar'):
            raise forms.ValidationError("Solo se permiten archivos en formato .rar para el Proyecto.")
        return proyecto

    def clean_Capitulos(self):
        capitulos = self.cleaned_data.get('Capitulos')
        if not capitulos.name.endswith('.rar'):
            raise forms.ValidationError("Solo se permiten archivos en formato .rar para los Capítulos.")
        return capitulos
