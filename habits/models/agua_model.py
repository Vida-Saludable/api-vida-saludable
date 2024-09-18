from django.db import models

from api.models import Usuario


class Agua(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    cantidad = models.IntegerField()  # En mililitros
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cantidad}ml ({self.fecha} {self.hora})"