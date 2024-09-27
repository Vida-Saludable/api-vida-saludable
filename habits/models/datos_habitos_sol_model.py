from django.db import models

from users.models.usuario_models import Usuario

class DatosHabitosSol(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    exposicion_sol_diaria = models.IntegerField(null=True, blank=True)
    exposicion_sol_horas_seguras = models.IntegerField(null=True, blank=True)
    exposicion_sol_20_minutos = models.IntegerField(null=True, blank=True)
    uso_bloqueador_solar = models.IntegerField(null=True, blank=True)
    
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  #inicial o final 

    def __str__(self):
        return f"Hábitos Sol de {self.usuario.correo}"