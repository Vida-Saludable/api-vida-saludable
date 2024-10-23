from django.db import models

from users.models.usuario_models import Usuario

class Alimentacion(models.Model):
    fecha = models.DateField()
    desayuno_hora = models.TimeField(null=True, blank=True)
    almuerzo_hora = models.TimeField(null=True, blank=True)
    cena_hora = models.TimeField(null=True, blank=True)
    desayuno = models.IntegerField(null=True, blank=True)  # Indica si hubo desayuno
    almuerzo = models.IntegerField(null=True, blank=True)  # Indica si hubo almuerzo
    cena = models.IntegerField(null=True, blank=True)      # Indica si hubo cena
    desayuno_saludable = models.IntegerField(null=True, blank=True)  # Cambiado a permitir nulos
    almuerzo_saludable = models.IntegerField(null=True, blank=True)  # Cambiado a permitir nulos
    cena_saludable = models.IntegerField(null=True, blank=True)      # Cambiado a permitir nulos
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha} ({self.usuario})"
