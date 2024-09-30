from django.db import models
from users.models.usuario_models import Usuario


class DatosFisicos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    altura = models.IntegerField(null=True, blank=True)
    imc = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    radio_abdominal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grasa_corporal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grasa_visceral = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    porcentaje_musculo = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  #inicial o final 

    def __str__(self):
        return f"Datos fisicos de {self.usuario.correo} ({self.tipo})"
