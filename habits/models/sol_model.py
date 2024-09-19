from django.db import models

from users.models.usuario_models import Usuario

class Sol(models.Model):
    fecha = models.DateField()
    tiempo = models.IntegerField()  # Cantidad de minutos
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tiempo} minutos ({self.fecha})"