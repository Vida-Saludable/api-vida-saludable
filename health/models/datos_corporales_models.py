from django.db import models
<<<<<<< HEAD
from ...users.models.usuario_models import Usuario
=======

from users.models.usuario_models import Usuario
>>>>>>> 19712261c84e3cd93c2de2304550f1bfd5f45941


class DatosCorporales(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    altura = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    imc = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    presion_sistolica = models.IntegerField(null=True, blank=True)
    presion_diastolica = models.IntegerField(null=True, blank=True)
    radio_abdominal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grasa_corporal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grasa_visceral = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    frecuencia_cardiaca = models.IntegerField(null=True, blank=True)
    frecuencia_respiratoria = models.IntegerField(null=True, blank=True)
    colesterol_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    colesterol_hdl = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    colesterol_ldl = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    trigliceridos = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    glucosa = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperatura = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    saturacion_oxigeno = models.IntegerField(null=True, blank=True)
    porcentaje_musculo = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    glicemia_basal = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    frecuencia_cardiaca_en_reposo = models.IntegerField(null=True, blank=True)
    frecuencia_cardiaca_despues_de_45_segundos = models.IntegerField(null=True, blank=True)
    frecuencia_cardiaca_1_minuto_despues = models.IntegerField(null=True, blank=True)
    resultado_test_rufier = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  #inicial o final 

    def __str__(self):
        return f"Datos corporales de {self.usuario.correo} ({self.tipo})"
