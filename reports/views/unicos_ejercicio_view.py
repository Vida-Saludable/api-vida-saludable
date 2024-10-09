from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from habits.models.ejercicio_model import Ejercicio

class EjercicioUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos de los campos 'tipo' y 'tiempo' del modelo Ejercicio
        tipos_ejercicio = Ejercicio.objects.values_list('tipo', flat=True).distinct()
        tiempos_ejercicio = Ejercicio.objects.values_list('tiempo', flat=True).distinct()

        # Crear la respuesta
        result = {
            'tipo': list(tipos_ejercicio),
            'tiempo': list(tiempos_ejercicio),
        }

        return Response(result, status=status.HTTP_200_OK)
