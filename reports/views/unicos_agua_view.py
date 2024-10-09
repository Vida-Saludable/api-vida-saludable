from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from habits.models.agua_model import Agua

class AguaUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos de los campos relacionados con agua
        horas = Agua.objects.values_list('hora', flat=True).distinct()
        cantidades = Agua.objects.values_list('cantidad', flat=True).distinct()

        # Crear la respuesta en un formato ordenado
        result = {
            'horas': list(horas),
            'cantidades': list(cantidades),
        }

        return Response(result, status=status.HTTP_200_OK)
