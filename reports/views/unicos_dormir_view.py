from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Min, Max
from habits.models.dormir_model import Dormir

class DormirUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos del campo 'hora' del modelo Dormir
        horas_unicas = Dormir.objects.values_list('hora', flat=True).distinct().order_by('hora')

        # Obtener la fecha mínima y máxima de los registros
        fecha_min = Dormir.objects.aggregate(min_fecha=Min('fecha'))['min_fecha']
        fecha_max = Dormir.objects.aggregate(max_fecha=Max('fecha'))['max_fecha']

        # Crear la respuesta
        result = {
            'hora': list(horas_unicas),
            'fecha_minima': fecha_min,
            'fecha_maxima': fecha_max
        }

        return Response(result, status=status.HTTP_200_OK)
