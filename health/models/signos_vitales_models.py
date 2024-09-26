from django.db import models
from users.models.usuario_models import Usuario


class SignosVitales(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    presion_sistolica = models.IntegerField(null=True, blank=True)
    presion_diastolica = models.IntegerField(null=True, blank=True)
    frecuencia_cardiaca = models.IntegerField(null=True, blank=True)
    frecuencia_respiratoria = models.IntegerField(null=True, blank=True)
    temperatura = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    saturacion_oxigeno = models.IntegerField(null=True, blank=True)
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  #inicial o final 

    def __str__(self):
        return f"Signos Vitales de {self.usuario.correo} ({self.tipo})"
