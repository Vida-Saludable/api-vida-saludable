from django.db import models

from users.models.usuario_models import Usuario


class Esperanza(models.Model):
    fecha = models.DateField()
    tipo_practica = models.CharField(max_length=50)  # oracion, leer la biblia
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo_practica} ({self.fecha})"