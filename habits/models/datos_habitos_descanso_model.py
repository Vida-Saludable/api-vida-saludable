from django.db import models

from users.models.usuario_models import Usuario

class DatosHabitosDescanso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    duermo_7_8_horas = models.IntegerField(null=True, blank=True)
    despertar_durante_noche = models.IntegerField(null=True, blank=True)
    dificultad_sueno_reparador = models.IntegerField(null=True, blank=True)
    horario_sueno_diario = models.IntegerField(null=True, blank=True)
    despertar_horario_diario = models.IntegerField(null=True, blank=True)

    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  #inicial o final 

   
    def __str__(self):
        return f"Hábitos Descanso de {self.usuario.correo}"