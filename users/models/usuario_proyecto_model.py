from django.db import models

from .proyecto_model import Proyecto
from .usuario_models import Usuario


class UsuarioProyecto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
   
    class Meta:
        unique_together = ('usuario', 'proyecto')

    def __str__(self):
        return f"{self.usuario} - {self.proyecto}"