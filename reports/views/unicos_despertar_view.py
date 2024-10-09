from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from habits.models.despertar_model import Despertar

class DespertarUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos de los campos 'hora' y 'estado' relacionados con despertar
        horas = Despertar.objects.values_list('hora', flat=True).distinct()
        estados = Despertar.objects.values_list('estado', flat=True).distinct()

        # Crear la respuesta en un formato ordenado
        result = {
            'horas': list(horas),
            'estados': list(estados),
        }

        return Response(result, status=status.HTTP_200_OK)
