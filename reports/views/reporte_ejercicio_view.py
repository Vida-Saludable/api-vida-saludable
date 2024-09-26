from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, F, Count
from django.db.models.functions import ExtractWeek, ExtractIsoWeekDay

from habits.models.ejercicio_model import Ejercicio
from ..serializers.reporte_ejercicio_serializer import ReporteEjercicioPorcetajeSerializer, ReporteEjercicioSerializer, ReporteEjercicioTipoSerializer


class ReporteEjercicioView(APIView):
    def get(self, request, usuario_id):
        # Verificar si el usuario existe
        if not Ejercicio.objects.filter(usuario_id=usuario_id).exists():
            return Response({"detail": "El usuario no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la tiempo total en minutos por día durante la semana
        queryset = (
            Ejercicio.objects
            .filter(usuario_id=usuario_id, fecha__week=ExtractWeek(F('fecha')))
            .annotate(
                fecha_dia=F('fecha'),  # Obtener la fecha completa
                dia_semana=ExtractIsoWeekDay(F('fecha'))  # Día de la semana
            )
            .values('fecha_dia', 'dia_semana')
            .annotate(tiempo_total=Sum('tiempo'))
            .order_by('fecha_dia')
        )

        serializer = ReporteEjercicioSerializer(queryset, many=True)
        return Response(serializer.data)


class ReporteEjercicioPorcentajeView(APIView):
    def get(self, request, usuario_id):
        # Verificar si el usuario tiene ejercicios registrados
        if not Ejercicio.objects.filter(usuario_id=usuario_id).exists():
            return Response(
                {
                    "success": False,
                    "message": "El usuario no tiene registros de ejercicio.",
                    "data": None
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Obtener todos los ejercicios del usuario
        ejercicios = Ejercicio.objects.filter(usuario_id=usuario_id)
        total_ejercicios = ejercicios.count()

        # Contar la cantidad de ejercicios de cada tipo
        tipo_ejercicios = (
            ejercicios
            .values('tipo')
            .annotate(conteo=Count('tipo'))
        )

        # Inicializar contadores para los tipos de ejercicio
        conteo_ejercicios = {
            'caminata lenta': 0,
            'caminata rapida': 0,
            'trote': 0,
            'ejercicio guiado': 0,
        }

        # Llenar los contadores con los valores reales
        for tipo in tipo_ejercicios:
            conteo_ejercicios[tipo['tipo']] = tipo['conteo']

        # Calcular los porcentajes de cada tipo de ejercicio como enteros
        def calcular_porcentaje(cantidad, total):
            return round((cantidad / total) * 100) if total > 0 else 0

        # Crear el diccionario de resultados con valores convertidos a enteros
        reporte = {
            'total_ejercicios': int(total_ejercicios),
            'caminata_lenta': int(calcular_porcentaje(conteo_ejercicios['caminata lenta'], total_ejercicios)),
            'caminata_rapida': int(calcular_porcentaje(conteo_ejercicios['caminata rapida'], total_ejercicios)),
            'trote': int(calcular_porcentaje(conteo_ejercicios['trote'], total_ejercicios)),
            'ejercicio_guiado': int(calcular_porcentaje(conteo_ejercicios['ejercicio guiado'], total_ejercicios)),
        }

        # Devolver la respuesta directamente con los datos ya convertidos a enteros
        return Response(
            {
                "success": True,
                "message": "Datos obtenidos correctamente",
                "data": reporte
            },
            status=status.HTTP_200_OK
        )


class ReporteEjercicioTipoView(APIView):
    def get(self, request, usuario_id, tipo_ejercicio):
        # Verificar si el usuario tiene ejercicios registrados de ese tipo
        if not Ejercicio.objects.filter(usuario_id=usuario_id, tipo=tipo_ejercicio).exists():
            return Response({"detail": "No se encontraron ejercicios para este usuario con el tipo especificado."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener el tiempo total en minutos por día durante la semana, filtrando por tipo
        queryset = (
            Ejercicio.objects
            .filter(usuario_id=usuario_id, tipo=tipo_ejercicio)  # Filtrar por usuario y tipo de ejercicio
            .annotate(
                fecha_dia=F('fecha'),  # Obtener la fecha completa
                dia_semana=ExtractIsoWeekDay(F('fecha'))  # Día de la semana como número (1-7)
            )
            .values('fecha_dia', 'dia_semana')  # Agrupar por fecha y día de la semana
            .annotate(tiempo_total=Sum('tiempo'))  # Sumar el tiempo total
            .order_by('fecha_dia')  # Ordenar por fecha
        )

        serializer = ReporteEjercicioTipoSerializer(queryset, many=True)
        return Response(serializer.data)