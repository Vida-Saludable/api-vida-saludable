from django.db import models
from django.forms import ValidationError


class Proyecto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.IntegerField(null=False, blank=False)

    def clean(self):
        if self.estado is not None and self.estado < 0:
            raise ValidationError({'estado': 'El estado no puede ser negativo'})
    
        if self.fecha_fin and self.fecha_inicio and self.fecha_fin < self.fecha_inicio:
            raise ValidationError({'fecha_fin': 'La fecha fin no puede ser anterior a la fecha inicio'})
    def __str__(self):
        return self.nombre