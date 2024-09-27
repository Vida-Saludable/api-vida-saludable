from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.datos_habitos_descanso_model import DatosHabitosDescanso
from ..serializers.datos_habitos_descanso_serializer import DatosHabitosDescansoSerializer


class DatosHabitosDescansoViewSet(viewsets.ModelViewSet):
    queryset = DatosHabitosDescanso.objects.all()
    serializer_class = DatosHabitosDescansoSerializer