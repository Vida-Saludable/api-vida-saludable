from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from habits.models.sol_model import Sol

class SolUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos del campo 'tiempo' y 'fecha' del modelo Sol
        tiempos_sol = Sol.objects.values_list('tiempo', flat=True).distinct()
        fechas_sol = Sol.objects.values_list('fecha', flat=True).distinct()

        # Crear la respuesta
        result = {
            'tiempo': list(tiempos_sol),
            'fecha': list(fechas_sol),
        }

        return Response(result, status=status.HTTP_200_OK)
