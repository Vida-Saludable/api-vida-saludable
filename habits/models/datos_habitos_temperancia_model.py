from django.db import models

from users.models.usuario_models import Usuario

class DatosHabitosTemperancia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    consumo_bebidas_alcoholicas = models.IntegerField(null=True, blank=True)
    eventos_sociales_alcohol = models.IntegerField(null=True, blank=True)
    consumo_sustancias_estimulantes = models.IntegerField(null=True, blank=True)
    consumo_refrescos_cola = models.IntegerField(null=True, blank=True)
    consumo_cigarrillos = models.IntegerField(null=True, blank=True)
    consumo_comida_chatarra = models.IntegerField(null=True, blank=True)
    pedir_mas_comida = models.IntegerField(null=True, blank=True)
    agregar_mas_azucar = models.IntegerField(null=True, blank=True)
    agregar_mas_sal = models.IntegerField(null=True, blank=True)
    satisfecho_trabajo = models.IntegerField(null=True, blank=True)
    tenso_nervioso_estresado = models.IntegerField(null=True, blank=True)
    tiempo_libre_redes_sociales = models.IntegerField(null=True, blank=True)
    satisfecho_relaciones_sociales = models.IntegerField(null=True, blank=True)
    apoyo_familia_decisiones = models.IntegerField(null=True, blank=True)

    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  #inicial o final 

    def __str__(self):
        return f"Hábitos Temperancia de {self.usuario.correo}"