from django.db import models
from users.models.usuario_models import Usuario


class DatosMuestras(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    colesterol_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    colesterol_hdl = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    colesterol_ldl = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    trigliceridos = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    glucosa = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    glicemia_basal = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  #inicial o final 

    def __str__(self):
        return f"Datos muestras de {self.usuario.correo} ({self.tipo})"
