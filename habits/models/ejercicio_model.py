from django.db import models

from users.models.usuario_models import Usuario

class Ejercicio(models.Model):
    fecha = models.DateField()
    tipo = models.CharField(max_length=50)  # caminata lenta, rápida, carrera, ejercicio guiado
    tiempo = models.IntegerField()  # Cantidad de minutos
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ejercicio ({self.tipo} - {self.fecha})"