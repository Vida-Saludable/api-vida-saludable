from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.datos_habitos_temperancia_model import DatosHabitosTemperancia
from ..serializers.datos_habitos_temperancia_serializer import DatosHabitosTemperanciaSerializer


class DatosHabitosTemperanciaViewSet(viewsets.ModelViewSet):
    queryset = DatosHabitosTemperancia.objects.all()
    serializer_class = DatosHabitosTemperanciaSerializer