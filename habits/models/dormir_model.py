from django.db import models

from api.models import Usuario

class Dormir(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sueño ({self.fecha} {self.hora})"