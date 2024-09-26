from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db.models.functions import ExtractIsoWeekDay

from habits.models.dormir_model import Dormir
from habits.models.despertar_model import Despertar
from ..serializers.reporte_descanso_serializer import ReporteHorasDormidasSerializer, ReportePorcentajeDescansoSerializer


class ReporteHorasDormidasView(APIView):
    def get(self, request, usuario_id):
        try:
            # Obtener registros de Dormir y Despertar para el usuario
            registros_dormir = Dormir.objects.filter(usuario_id=usuario_id)
            registros_despertar = Despertar.objects.filter(usuario_id=usuario_id)

            # Anotar el día de la semana para los registros de dormir
            registros_dormir = registros_dormir.annotate(
                dia_semana=ExtractIsoWeekDay('fecha')
            )

            resultados = []

            for dormir in registros_dormir:
                despertar = registros_despertar.filter(
                    fecha=dormir.fecha,
                    hora__gte=dormir.hora
                ).order_by('hora').first()

                if not despertar:
                    despertar = registros_despertar.filter(
                        fecha=dormir.fecha + timedelta(days=1),
                        hora__lt=dormir.hora
                    ).order_by('hora').first()

                if despertar:
                    # Calcular el tiempo dormido
                    hora_dormir = datetime.combine(dormir.fecha, dormir.hora)
                    hora_despertar = datetime.combine(despertar.fecha, despertar.hora)

                    if hora_despertar < hora_dormir:
                        hora_despertar += timedelta(days=1)  # Ajustar si la hora de despertar es al día siguiente

                    tiempo_dormido = (hora_despertar - hora_dormir).total_seconds()
                    total_horas = tiempo_dormido // 3600
                    total_minutos = (tiempo_dormido % 3600) // 60

                    fecha_dia = dormir.fecha.strftime('%Y-%m-%d')
                    dia_semana = dormir.dia_semana  # Extraído por ExtractIsoWeekDay

                    resultados.append({
                        'fecha_dia': fecha_dia,
                        'dia_semana': dia_semana,
                        'total_horas': int(total_horas),
                        'total_minutos': int(total_minutos)
                    })

            serializer = ReporteHorasDormidasSerializer(resultados, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error:", str(e))
            return Response({"detail": "Error al procesar los datos."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ReportePorcentajeDescansoView(APIView):
    def get(self, request, usuario_id):
        try:
            registros = Despertar.objects.filter(usuario_id=usuario_id)
            
            if not registros.exists():
                return Response({
                    "success": False, 
                    "message": "No hay registros de despertar para este usuario."
                }, status=status.HTTP_404_NOT_FOUND)

            total_registros = registros.count()
            
            conteo_estados = registros.values('estado').annotate(total=Count('estado'))
            estado_counts = {estado['estado']: estado['total'] for estado in conteo_estados}

            estado_0_count = estado_counts.get(0, 0)
            estado_1_count = estado_counts.get(1, 0)

            descanso_mal = (estado_0_count / total_registros) * 100
            descanso_bien = (estado_1_count / total_registros) * 100

            resultado = {
                "total_registros": total_registros,
                "descanso_mal": round(descanso_mal, 2),
                "descanso_bien": round(descanso_bien, 2)
            }

            return Response({
                "success": True,
                "message": "Datos procesados correctamente.",
                "data": resultado
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error:", str(e))
            return Response({
                "success": False, 
                "message": "Error al procesar los datos."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)