from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.datos_habitos_esperanza_model import DatosHabitosEsperanza
from ..serializers.datos_habitos_esperanza_serializer import DatosHabitosEsperanzaSerializer


class DatosHabitosEsperanzaViewSet(viewsets.ModelViewSet):
    queryset = DatosHabitosEsperanza.objects.all()
    serializer_class = DatosHabitosEsperanzaSerializer