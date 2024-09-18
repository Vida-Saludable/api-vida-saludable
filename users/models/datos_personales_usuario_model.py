from django.db import models

from users.models.usuario_models import Usuario

class DatosPersonalesUsuario(models.Model):
    nombres_apellidos = models.CharField(max_length=255, null=True, blank=True)
    sexo = models.CharField(max_length=10, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    estado_civil = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=100, null=True, blank=True)
    grado_instruccion = models.CharField(max_length=50, null=True, blank=True)
    procedencia = models.CharField(max_length=100, null=True, blank=True)
    religion = models.CharField(max_length=50, null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)



    def __str__(self):
        return f"{self.nombres_apellidos} - {self.usuario.correo}"