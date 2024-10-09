from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from habits.models.aire_model import Aire

class AireUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos del campo "tiempo" relacionado con aire
        tiempos = Aire.objects.values_list('tiempo', flat=True).distinct()

        # Crear la respuesta en un formato ordenado
        result = {
            'tiempos': list(tiempos),
        }

        return Response(result, status=status.HTTP_200_OK)
