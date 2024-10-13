from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Min, Max
from habits.models.alimentacion_model import Alimentacion

class AlimentacionUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos de los campos relacionados con alimentación
        desayuno_horas = Alimentacion.objects.values_list('desayuno_hora', flat=True).distinct().order_by('desayuno_hora')
        almuerzo_horas = Alimentacion.objects.values_list('almuerzo_hora', flat=True).distinct().order_by('almuerzo_hora')
        cena_horas = Alimentacion.objects.values_list('cena_hora', flat=True).distinct().order_by('cena_hora')
        desayunos = Alimentacion.objects.values_list('desayuno', flat=True).distinct()
        almuerzos = Alimentacion.objects.values_list('almuerzo', flat=True).distinct()
        cenas = Alimentacion.objects.values_list('cena', flat=True).distinct()
        desayunos_saludables = Alimentacion.objects.values_list('desayuno_saludable', flat=True).distinct()
        almuerzos_saludables = Alimentacion.objects.values_list('almuerzo_saludable', flat=True).distinct()
        cenas_saludables = Alimentacion.objects.values_list('cena_saludable', flat=True).distinct()

        # Obtener las fechas mínima y máxima
        fecha_min = Alimentacion.objects.aggregate(min_fecha=Min('fecha'))['min_fecha']
        fecha_max = Alimentacion.objects.aggregate(max_fecha=Max('fecha'))['max_fecha']

        # Crear la respuesta en un formato ordenado
        result = {
            'desayuno_hora': list(desayuno_horas),
            'almuerzo_hora': list(almuerzo_horas),
            'cena_hora': list(cena_horas),
            'desayuno': list(desayunos),
            'almuerzo': list(almuerzos),
            'cena': list(cenas),
            'desayuno_saludable': list(desayunos_saludables),
            'almuerzo_saludable': list(almuerzos_saludables),
            'cena_saludable': list(cenas_saludables),
            'fecha_minima': fecha_min,
            'fecha_maxima': fecha_max
        }

        return Response(result, status=status.HTTP_200_OK)
