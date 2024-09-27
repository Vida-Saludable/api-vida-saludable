from django.db import models

from users.models.usuario_models import Usuario

class DatosHabitosAgua(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    bebo_solo_agua_pura = models.IntegerField(null=True, blank=True)
    bebo_8_vasos_agua = models.IntegerField(null=True, blank=True)
    bebidas_con_azucar = models.IntegerField(null=True, blank=True)
    bebo_agua_al_despertar = models.IntegerField(null=True, blank=True)
    bebo_agua_antes_comidas = models.IntegerField(null=True, blank=True)
    bebo_agua_para_dormir = models.IntegerField(null=True, blank=True)
    
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  #inicial o final 

    def __str__(self):
        return f"Hábitos Agua de {self.usuario.correo}"