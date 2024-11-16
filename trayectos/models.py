from django.db import models
from accounts.models import Estudiante  # Asegúrate de que esta importación no cause problemas circulares


class Trayectos_all(models.Model):
    ref_cedula = models.ForeignKey(Estudiante, on_delete=models.CASCADE)  # Relación con estudiante
    ci_est = models.CharField(max_length=10)
    name_est = models.CharField(max_length=32)
    seccion = models.CharField(max_length=10)
    trayecto_año = models.CharField(max_length=10)
    codigo_año = models.CharField(max_length=10)

    def __str__(self):
        return self.ci_est + ' - ' + self.name_est + ' - ' + self.seccion

    class Meta:
        db_table = 'trayectos_all'


class Trayecto1(models.Model):
    ref_cedula = models.ForeignKey(Estudiante, on_delete=models.CASCADE)  # Relación con estudiante
    ci_est = models.CharField(max_length=10)
    name_est = models.CharField(max_length=32)
    seccion = models.CharField(max_length=10)

    def __str__(self):
        return self.ci_est + ' - ' + self.name_est + ' - ' + self.seccion

    class Meta:
        db_table = 'trayecto1'

class Trayecto2(models.Model):
    ref_cedula = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    ci_est = models.CharField(max_length=10)
    name_est = models.CharField(max_length=32)
    seccion = models.CharField(max_length=10)

    def __str__(self):
        return self.ci_est + ' - ' + self.name_est + ' - ' + self.seccion
    
    class Meta:
        db_table = 'trayecto2'

class Trayecto3(models.Model):
    ref_cedula = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    ci_est = models.CharField(max_length=10)
    name_est = models.CharField(max_length=32)
    seccion = models.CharField(max_length=10)

    def __str__(self):
        return self.ci_est + ' - ' + self.name_est + ' - ' + self.seccion
    
    class Meta:
        db_table = 'trayecto3'

class Trayecto4(models.Model):
    ref_cedula = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    ci_est = models.CharField(max_length=10)
    name_est = models.CharField(max_length=32)
    seccion = models.CharField(max_length=10)

    def __str__(self):
        return self.ci_est + ' - ' + self.name_est + ' - ' + self.seccion
    
    class Meta:
        db_table = 'trayecto4'

class EtapasEstudiantes(models.Model):
    Fecha = models.DateField()
    Estatus = models.CharField(max_length=16)
    Grupo_est_id = models.CharField(max_length=50)  # Simulación de ForeignKey como CharField

    def __str__(self):
        return f"{self.Estatus} - {self.Grupo_est_id}"


class ArchivosEstudiantes(models.Model):
    Proyecto = models.FileField(upload_to='proyectos/')
    Capitulos = models.FileField(upload_to='capitulos/')
    Grupo_est_id = models.CharField(max_length=50)  # Simulación de ForeignKey como CharField

    def __str__(self):
        return f"Archivo {self.id} del grupo {self.Grupo_est_id}"
