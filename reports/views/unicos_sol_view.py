from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Min, Max
from habits.models.sol_model import Sol

class SolUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos del campo 'tiempo' y 'fecha' del modelo Sol
        tiempos_sol = Sol.objects.values_list('tiempo', flat=True).distinct().order_by('tiempo')
        fechas_sol = Sol.objects.values_list('fecha', flat=True).distinct()

        # Obtener la fecha mínima y máxima de los registros
        fecha_minima = Sol.objects.aggregate(min_fecha=Min('fecha'))['min_fecha']
        fecha_maxima = Sol.objects.aggregate(max_fecha=Max('fecha'))['max_fecha']

        # Crear la respuesta
        result = {
            'tiempo': list(tiempos_sol),
            'fecha': list(fechas_sol),
            'fecha_minima': fecha_minima,
            'fecha_maxima': fecha_maxima,
        }

        return Response(result, status=status.HTTP_200_OK)
