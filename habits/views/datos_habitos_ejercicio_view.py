from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.datos_habitos_ejercicio_model import DatosHabitosEjercicio
from ..serializers.datos_habitos_ejercicio_serializer import DatosHabitosEjercicioSerializer


class DatosHabitosEjercicioViewSet(viewsets.ModelViewSet):
    queryset = DatosHabitosEjercicio.objects.all()
    serializer_class = DatosHabitosEjercicioSerializer