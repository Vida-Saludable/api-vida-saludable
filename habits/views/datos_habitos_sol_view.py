from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.datos_habitos_sol_model import DatosHabitosSol
from ..serializers.datos_habitos_sol_serializer import DatosHabitosSolSerializer


class DatosHabitosSolViewSet(viewsets.ModelViewSet):
    queryset = DatosHabitosSol.objects.all()
    serializer_class = DatosHabitosSolSerializer