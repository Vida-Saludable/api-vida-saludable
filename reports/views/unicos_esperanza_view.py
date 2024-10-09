from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from habits.models.esperanza_model import Esperanza

class EsperanzaUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos del campo 'tipo_practica' y 'fecha' del modelo Esperanza
        tipos_practica = Esperanza.objects.values_list('tipo_practica', flat=True).distinct()
        fechas_practica = Esperanza.objects.values_list('fecha', flat=True).distinct()

        # Crear la respuesta
        result = {
            'tipo_practica': list(tipos_practica),
            'fecha': list(fechas_practica),
        }

        return Response(result, status=status.HTTP_200_OK)
