from django.db import models

from users.models.usuario_models import Usuario

class DatosHabitosEjercicio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    realizo_actividad_deportiva = models.IntegerField(null=True, blank=True)
    ejercicio_fisico_diario = models.IntegerField(null=True, blank=True)
    practico_deporte_tiempo_libre = models.IntegerField(null=True, blank=True)
    dedicacion_30_minutos_ejercicio = models.IntegerField(null=True, blank=True)
    ejercicio_carrera_bicicleta = models.IntegerField(null=True, blank=True)
    
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  #inicial o final 


    def __str__(self):
        return f"Hábitos Ejercicios de {self.usuario.correo}"