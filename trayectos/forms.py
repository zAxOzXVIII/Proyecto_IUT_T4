from django import forms
from django.core.exceptions import ValidationError
import re
from accounts.models import Estudiante  # O el modelo correspondiente

class AsignarEstudiantesForm(forms.Form):
    estudiantes = forms.ModelMultipleChoiceField(queryset=Estudiante.objects.all(), widget=forms.CheckboxSelectMultiple)
    seccion = forms.CharField(max_length=10)

    def clean_seccion(self):
        seccion = self.cleaned_data.get('seccion')
        return seccion
