from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.datos_habitos_agua_model import DatosHabitosAgua
from ..serializers.datos_habitos_agua_serializer import DatosHabitosAguaSerializer


class DatosHabitosAguaViewSet(viewsets.ModelViewSet):
    queryset = DatosHabitosAgua.objects.all()
    serializer_class = DatosHabitosAguaSerializer