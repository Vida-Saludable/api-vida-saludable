from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import ROUND_HALF_UP, Decimal
from users.models.usuario_models import Usuario

class DatosFisicos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    altura = models.IntegerField(null=True, blank=True)
    imc = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, editable=False)
    radio_abdominal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grasa_corporal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grasa_visceral = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    porcentaje_musculo = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  # inicial o final

    def __str__(self):
        return f"Datos fisicos de {self.usuario.correo} ({self.tipo})"

    def calcular_imc(self):
        """Calcula el IMC basado en peso y altura con redondeo a 2 decimales"""
        if self.peso and self.altura:
            altura_metros = Decimal(self.altura) / Decimal(100)  # Convertir cm a m
            imc_calculado = self.peso / (altura_metros ** 2)
            return imc_calculado.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return None

@receiver(pre_save, sender=DatosFisicos)
def actualizar_imc(sender, instance, **kwargs):
    """Señal para calcular automáticamente el IMC antes de guardar"""
    instance.imc = instance.calcular_imc()