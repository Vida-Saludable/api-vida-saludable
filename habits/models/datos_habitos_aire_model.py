from django.db import models

from users.models.usuario_models import Usuario

class DatosHabitosAire(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    tecnica_respiraciones_profundas = models.IntegerField(null=True, blank=True)
    tiempo_tecnica_respiraciones = models.IntegerField(null=True, blank=True)
    horario_tecnica_respiraciones_manana = models.IntegerField(null=True, blank=True)
    horario_tecnica_respiraciones_noche = models.IntegerField(null=True, blank=True)
    
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  #inicial o final 


    def __str__(self):
        return f"Hábitos Aire de {self.usuario.correo}"