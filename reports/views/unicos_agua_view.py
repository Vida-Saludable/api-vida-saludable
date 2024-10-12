from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Min, Max
from habits.models.agua_model import Agua

class AguaUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos de los campos relacionados con agua
        horas = Agua.objects.values_list('hora', flat=True).distinct()
        cantidades = Agua.objects.values_list('cantidad', flat=True).distinct()

        # Obtener las fechas mínima y máxima
        fecha_min = Agua.objects.aggregate(min_fecha=Min('fecha'))['min_fecha']
        fecha_max = Agua.objects.aggregate(max_fecha=Max('fecha'))['max_fecha']

        # Crear la respuesta en un formato ordenado
        result = {
            'horas': list(horas),
            'cantidades': list(cantidades),
            'fecha_minima': fecha_min,
            'fecha_maxima': fecha_max,
        }

        return Response(result, status=status.HTTP_200_OK)
