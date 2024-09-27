from django.db import models

from users.models.usuario_models import Usuario

class DatosHabitosEsperanza(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    ser_supremo_interviene = models.IntegerField(null=True, blank=True)
    leo_biblia = models.IntegerField(null=True, blank=True)
    practico_oracion = models.IntegerField(null=True, blank=True)
    orar_y_estudiar_biblia_desarrollo_personal = models.IntegerField(null=True, blank=True)
    
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  #inicial o final 


    def __str__(self):
        return f"Hábitos Esperanza de {self.usuario.correo}"