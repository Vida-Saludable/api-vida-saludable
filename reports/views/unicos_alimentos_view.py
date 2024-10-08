from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from habits.models.alimentacion_model import Alimentacion
from django.db.models import F

class AlimentacionUnicosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener los valores únicos de los campos relacionados con alimentación de todos los usuarios
        desayuno_horas = Alimentacion.objects.values_list('desayuno_hora', flat=True).distinct()
        almuerzo_horas = Alimentacion.objects.values_list('almuerzo_hora', flat=True).distinct()
        cena_horas = Alimentacion.objects.values_list('cena_hora', flat=True).distinct()
        desayunos = Alimentacion.objects.values_list('desayuno', flat=True).distinct()
        almuerzos = Alimentacion.objects.values_list('almuerzo', flat=True).distinct()
        cenas = Alimentacion.objects.values_list('cena', flat=True).distinct()
        desayunos_saludables = Alimentacion.objects.values_list('desayuno_saludable', flat=True).distinct()
        almuerzos_saludables = Alimentacion.objects.values_list('almuerzo_saludable', flat=True).distinct()
        cenas_saludables = Alimentacion.objects.values_list('cena_saludable', flat=True).distinct()

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
        }

        return Response(result, status=status.HTTP_200_OK)
