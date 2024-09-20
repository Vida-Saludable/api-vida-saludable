from rest_framework import status
from rest_framework import viewsets
from datetime import datetime, timedelta
from rest_framework.response import Response

from ..models.dormir_model import Dormir
from ..models.despertar_model import Despertar
from ..serializers.dormir_serializer import DormirSerializer
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario


class DormirViewSet(viewsets.ModelViewSet):
    queryset = Dormir.objects.all()
    serializer_class = DormirSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'success': True,
            'message': 'Se registró exitosamente',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        resultados = []
        usuario_info = {}

        for dormir in queryset:
            usuario_id = dormir.usuario.id
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()

            # Agrupar por fecha
            fecha_str = dormir.fecha.strftime("%Y-%m-%d")
            if fecha_str not in usuario_info:
                usuario_info[fecha_str] = {
                    "fecha": fecha_str,
                    "usuario": datos_personales.nombres_apellidos if datos_personales else None,
                    "telefono": datos_personales.telefono if datos_personales else None,
                    "total_horas": 0,
                    "total_minutos": 0,
                    "hora_dormir": dormir.hora.strftime("%H:%M:%S"),
                    "hora_despertar": None,  # Inicializar
                }

            # Obtener registros de despertar para la fecha actual
            registros_despertar = Despertar.objects.filter(usuario_id=usuario_id)

            for despertar in registros_despertar:
                if despertar.fecha >= dormir.fecha:  # Considerar solo despertares después de dormir
                    hora_dormir = datetime.combine(dormir.fecha, dormir.hora)
                    hora_despertar = datetime.combine(despertar.fecha, despertar.hora)

                    # Ajustar si la hora de despertar es al día siguiente
                    if hora_despertar < hora_dormir:
                        hora_despertar += timedelta(days=1)

                    # Calcular el tiempo dormido
                    tiempo_dormido = (hora_despertar - hora_dormir).total_seconds()
                    total_horas = tiempo_dormido // 3600
                    total_minutos = (tiempo_dormido % 3600) // 60

                    usuario_info[fecha_str]["total_horas"] += int(total_horas)
                    usuario_info[fecha_str]["total_minutos"] += int(total_minutos)

                    # Guardar la última hora de despertar
                    usuario_info[fecha_str]["hora_despertar"] = despertar.hora.strftime("%H:%M:%S")

        # Convertir el diccionario a lista
        for item in usuario_info.values():
            resultados.append(item)

        return Response({
            'success': True,
            'message': 'Listado de registros de dormir',
            'data': resultados
        })
