from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Min, Max
from habits.models.esperanza_model import Esperanza

class EsperanzaUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos del campo 'tipo_practica' y 'fecha' del modelo Esperanza
        tipos_practica = Esperanza.objects.values_list('tipo_practica', flat=True).distinct()
        fechas_practica = Esperanza.objects.values_list('fecha', flat=True).distinct()

        # Obtener la fecha mínima y máxima de los registros
        fecha_min = Esperanza.objects.aggregate(min_fecha=Min('fecha'))['min_fecha']
        fecha_max = Esperanza.objects.aggregate(max_fecha=Max('fecha'))['max_fecha']

        # Crear la respuesta
        result = {
            'tipo_practica': list(tipos_practica),
            'fecha': list(fechas_practica),
            'fecha_minima': fecha_min,
            'fecha_maxima': fecha_max,
        }

        return Response(result, status=status.HTTP_200_OK)
