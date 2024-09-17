from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Min, Max

from ..models import Alimentacion

class GetDatesByIdView(APIView):
    def get(self, request, *args, **kwargs):
        usuario_id = self.kwargs.get('usuario_id')

        # Obtener las fechas mínimas y máximas para el hábito de alimentación del usuario
        fechas = Alimentacion.objects.filter(usuario_id=usuario_id).aggregate(
            primera_fecha=Min('fecha'), ultima_fecha=Max('fecha')
        )

        return Response(fechas, status=status.HTTP_200_OK)

