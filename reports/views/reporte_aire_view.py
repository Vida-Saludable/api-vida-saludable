from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, F
from django.db.models.functions import ExtractWeek, ExtractIsoWeekDay

from habits.models.aire_model import Aire
from ..serializers.reporte_aire_serializer import ReporteAireSerializer


class ReporteAireView(APIView):
    def get(self, request, usuario_id):
        # Verificar si el usuario existe
        if not Aire.objects.filter(usuario_id=usuario_id).exists():
            return Response({"detail": "El usuario no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la tiempo total en minutos por día durante la semana
        queryset = (
            Aire.objects
            .filter(usuario_id=usuario_id, fecha__week=ExtractWeek(F('fecha')))
            .annotate(
                fecha_dia=F('fecha'),  # Obtener la fecha completa
                dia_semana=ExtractIsoWeekDay(F('fecha'))  # Día de la semana
            )
            .values('fecha_dia', 'dia_semana')
            .annotate(tiempo_total=Sum('tiempo'))
            .order_by('fecha_dia')
        )

        serializer = ReporteAireSerializer(queryset, many=True)
        return Response(serializer.data)