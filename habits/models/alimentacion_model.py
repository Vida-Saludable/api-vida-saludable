from django.db import models

from users.models.usuario_models import Usuario

class Alimentacion(models.Model):
    fecha = models.DateField()
    desayuno_hora = models.TimeField()
    almuerzo_hora = models.TimeField()
    cena_hora = models.TimeField()
    desayuno = models.IntegerField()  # Indica si hubo desayuno
    almuerzo = models.IntegerField()  # Indica si hubo almuerzo
    cena = models.IntegerField()      # Indica si hubo cena
    # Cambiar los campos de string a booleanos para indicar si fue saludable
    desayuno_saludable = models.IntegerField() 
    almuerzo_saludable = models.IntegerField()
    cena_saludable = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo_alimento} ({self.fecha} {self.hora})"