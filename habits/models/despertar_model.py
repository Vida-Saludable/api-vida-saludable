from django.db import models

from api.models import Usuario

class Despertar(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Despertar ({self.fecha} {self.hora})"