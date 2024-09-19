from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count

from habits.models.esperanza_model import Esperanza
from ..serializers.reporte_esperanza_serializer import ReporteEsperanzaPorcentajeSerializer


class ReporteEsperanzaPorcentajeView(APIView):
    def get(self, request, usuario_id):
        # Verificar si el usuario tiene registros de esperanza
        if not Esperanza.objects.filter(usuario_id=usuario_id).exists():
            return Response({"detail": "El usuario no tiene registros de esperanza."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener todos los registros de esperanza del usuario
        esperanzas = Esperanza.objects.filter(usuario_id=usuario_id)
        total_tipo = esperanzas.count()

        # Contar la cantidad de registros por tipo de práctica
        tipo_esperanzas = (
            esperanzas
            .values('tipo_practica')
            .annotate(conteo=Count('tipo_practica'))
        )

        # Inicializar contadores para los tipos de práctica
        conteo_esperanzas = {
            'oracion': 0,
            'lectura biblica': 0,
        }

        # Llenar los contadores con los valores reales
        for tipo in tipo_esperanzas:
            conteo_esperanzas[tipo['tipo_practica']] = tipo['conteo']

        # Calcular los porcentajes de cada tipo de práctica
        def calcular_porcentaje(cantidad, total):
            return round((cantidad / total) * 100, 2) if total > 0 else 0

        # Crear el diccionario de resultados
        reporte = {
            'total_tipo': total_tipo,
            'tipo_oracion': calcular_porcentaje(conteo_esperanzas['oracion'], total_tipo),
            'tipo_lectura': calcular_porcentaje(conteo_esperanzas['lectura biblica'], total_tipo),
        }

        # Serializar los datos y devolver la respuesta
        serializer = ReporteEsperanzaPorcentajeSerializer(reporte)
        return Response(serializer.data)