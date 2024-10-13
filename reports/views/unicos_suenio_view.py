from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from habits.models.dormir_model import Dormir
from habits.models.despertar_model import Despertar

class SuenioUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos de las horas de dormir y despertar
        dormir_horas = Dormir.objects.values_list('hora', flat=True).distinct().order_by('hora')
        despertar_horas = Despertar.objects.values_list('hora', flat=True).distinct()

        # Crear la respuesta
        result = {
            'hora_dormir': list(dormir_horas),
            'hora_despertar': list(despertar_horas),
        }

        return Response(result, status=status.HTTP_200_OK)
