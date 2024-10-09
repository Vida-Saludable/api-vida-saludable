from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from habits.models.dormir_model import Dormir

class DormirUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos del campo 'hora' del modelo Dormir
        horas_unicas = Dormir.objects.values_list('hora', flat=True).distinct()

        # Crear la respuesta
        result = {
            'hora': list(horas_unicas),
        }

        return Response(result, status=status.HTTP_200_OK)
