from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Min, Max
from habits.models.despertar_model import Despertar

class DespertarUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos de los campos 'hora' y 'estado'
        horas = Despertar.objects.values_list('hora', flat=True).distinct().order_by('hora')
        estados = Despertar.objects.values_list('estado', flat=True).distinct()

        # Obtener fechas mínima y máxima de los registros
        fecha_min = Despertar.objects.aggregate(min_fecha=Min('fecha'))['min_fecha']
        fecha_max = Despertar.objects.aggregate(max_fecha=Max('fecha'))['max_fecha']

        # Crear la respuesta en un formato ordenado
        result = {
            'horas': list(horas),
            'estados': list(estados),
            'fecha_minima': fecha_min,
            'fecha_maxima': fecha_max
        }

        return Response(result, status=status.HTTP_200_OK)
