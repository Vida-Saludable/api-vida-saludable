from django.db import models

from users.models.usuario_models import Usuario

class DatosHabitosAlimentacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    consumo_3_comidas_horario_fijo = models.IntegerField(null=True, blank=True)
    consumo_5_porciones_frutas_verduras = models.IntegerField(null=True, blank=True)
    consumo_3_porciones_proteinas = models.IntegerField(null=True, blank=True)
    ingiero_otros_alimentos = models.IntegerField(null=True, blank=True)
    consumo_carbohidratos = models.IntegerField(null=True, blank=True)
    consumo_alimentos_fritos = models.IntegerField(null=True, blank=True)
    consumo_alimentos_hechos_en_casa = models.IntegerField(null=True, blank=True)
    consumo_liquidos_mientras_como = models.IntegerField(null=True, blank=True)

    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  #inicial o final 


    def __str__(self):
        return f"Hábitos Alimentacion de {self.usuario.correo}"