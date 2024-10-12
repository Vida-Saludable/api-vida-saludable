from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Min, Max
from habits.models.aire_model import Aire

class AireUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos del campo "tiempo"
        tiempos = Aire.objects.values_list('tiempo', flat=True).distinct()

        # Obtener las fechas mínima y máxima
        fecha_min = Aire.objects.aggregate(min_fecha=Min('fecha'))['min_fecha']
        fecha_max = Aire.objects.aggregate(max_fecha=Max('fecha'))['max_fecha']

        # Crear la respuesta en un formato ordenado
        result = {
            'tiempos': list(tiempos),
            'fecha_minima': fecha_min,
            'fecha_maxima': fecha_max,
        }

        return Response(result, status=status.HTTP_200_OK)
