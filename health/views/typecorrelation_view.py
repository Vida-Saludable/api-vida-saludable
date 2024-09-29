from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from health.models.datos_fisicos_models import DatosFisicos
from habits.models.datos_habitos_alimentacion_model import DatosHabitosAlimentacion

class TiposDeCorrelacionView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los tipos únicos de DatosFisicos
        tipos_datos_fisicos = DatosFisicos.objects.values_list('tipo', flat=True).distinct()

        # Obtener los tipos únicos de DatosHabitosAlimentacion
        tipos_datos_habitos_alimentacion = DatosHabitosAlimentacion.objects.values_list('tipo', flat=True).distinct()

        # Combinar ambas listas y eliminar duplicados
        todos_los_tipos = list(set(tipos_datos_fisicos) | set(tipos_datos_habitos_alimentacion))

        # Devolver la lista como respuesta
        return Response(todos_los_tipos, status=status.HTTP_200_OK)
