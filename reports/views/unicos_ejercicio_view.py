from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Min, Max
from habits.models.ejercicio_model import Ejercicio

class EjercicioUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos de los campos 'tipo' y 'tiempo' del modelo Ejercicio
        tipos_ejercicio = Ejercicio.objects.values_list('tipo', flat=True).distinct()
        tiempos_ejercicio = Ejercicio.objects.values_list('tiempo', flat=True).distinct()

        # Obtener la fecha mínima y máxima de los registros
        fecha_min = Ejercicio.objects.aggregate(min_fecha=Min('fecha'))['min_fecha']
        fecha_max = Ejercicio.objects.aggregate(max_fecha=Max('fecha'))['max_fecha']

        # Crear la respuesta
        result = {
            'tipo': list(tipos_ejercicio),
            'tiempo': list(tiempos_ejercicio),
            'fecha_minima': fecha_min,
            'fecha_maxima': fecha_max,
        }

        return Response(result, status=status.HTTP_200_OK)
