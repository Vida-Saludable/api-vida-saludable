from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.datos_habitos_aire_model import DatosHabitosAire
from ..serializers.datos_habitos_aire_serializer import DatosHabitosAireSerializer


class DatosHabitosAireViewSet(viewsets.ModelViewSet):
    queryset = DatosHabitosAire.objects.all()
    serializer_class = DatosHabitosAireSerializer