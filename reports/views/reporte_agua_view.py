from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, F
from django.db.models.functions import ExtractWeek, ExtractIsoWeekDay

from ...habits.models.agua_model import Agua
from ..serializers.reporte_agua_serializer import ReporteAguaSerializer

class ReporteAguaView(APIView):
    def get(self, request, usuario_id):
        # Verificar si el usuario existe
        if not Agua.objects.filter(usuario_id=usuario_id).exists():
            return Response({"detail": "El usuario no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la cantidad de agua tomada por día durante la semana
        queryset = (
            Agua.objects
            .filter(usuario_id=usuario_id, fecha__week=ExtractWeek(F('fecha')))
            .annotate(
                fecha_dia=F('fecha'),  # Obtener la fecha completa
                dia_semana=ExtractIsoWeekDay(F('fecha'))  # Día de la semana
            )
            .values('fecha_dia', 'dia_semana')
            .annotate(cantidad_agua=Sum('cantidad'))
            .order_by('fecha_dia')
        )

        serializer = ReporteAguaSerializer(queryset, many=True)
        return Response(serializer.data)