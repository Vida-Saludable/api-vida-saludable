from django.db import models
from users.models.usuario_models import Usuario


class TestRuffier(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    frecuencia_cardiaca_en_reposo = models.IntegerField(null=True, blank=True)
    frecuencia_cardiaca_despues_de_45_segundos = models.IntegerField(null=True, blank=True)
    frecuencia_cardiaca_1_minuto_despues = models.IntegerField(null=True, blank=True)
    resultado_test_ruffier = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  #inicial o final 

    def __str__(self):
        return f"Test Ruffier de {self.usuario.correo} ({self.tipo})"
