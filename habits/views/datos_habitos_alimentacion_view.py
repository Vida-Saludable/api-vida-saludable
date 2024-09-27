from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.datos_habitos_alimentacion_model import DatosHabitosAlimentacion
from ..serializers.datos_habitos_alimentacion_serializer import DatosHabitosAlimentacionSerializer


class DatosHabitosAlimentacionViewSet(viewsets.ModelViewSet):
    queryset = DatosHabitosAlimentacion.objects.all()
    serializer_class = DatosHabitosAlimentacionSerializer