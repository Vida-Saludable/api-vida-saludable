from rest_framework import viewsets, status
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from ..models.dormir_model import Dormir
from ..models.despertar_model import Despertar
from ..serializers.dormir_serializer import DormirSerializer
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario

class CustomPagination(PageNumberPagination):
    page_size = 7  # Número de elementos por página
    page_size_query_param = 'page_size'  # Permite a los usuarios definir el tamaño de página en la solicitud
    max_page_size = 100  # Tamaño máximo de la página

class DormirViewSet(viewsets.ModelViewSet):
    queryset = Dormir.objects.all()
    serializer_class = DormirSerializer
    pagination_class = CustomPagination

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
        # Obtener parámetros de búsqueda
        usuario = request.query_params.get('usuario', None)
        proyecto_id = request.query_params.get('proyecto', None)

        # Obtener el queryset base y ordenarlo
        queryset = self.get_queryset().order_by('fecha')

        # Filtrar por usuario
        if usuario:
            queryset = queryset.filter(usuario__datospersonalesusuario__nombres_apellidos__icontains=usuario)

        # Filtrar por proyecto
        if proyecto_id:
            queryset = queryset.filter(usuario__usuarioproyecto__proyecto__id=proyecto_id).distinct()

        # Aplicar paginación al queryset base
        paginated_queryset = self.paginate_queryset(queryset)

        # Procesar solo los datos paginados
        usuario_info = []
        for dormir in paginated_queryset:
            usuario_id = dormir.usuario.id
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()

            # Construir los datos iniciales
            item = {
                "id": dormir.id,  # Incluir el ID del registro de dormir
                "fecha": dormir.fecha.strftime("%Y-%m-%d"),
                "usuario": datos_personales.nombres_apellidos if datos_personales else None,
                "telefono": datos_personales.telefono if datos_personales else None,
                "total_horas": 0,
                "total_minutos": 0,
                "hora_dormir": dormir.hora.strftime("%H:%M:%S"),
                "hora_despertar": None,
                "estado": None
            }

            # Obtener registros de despertar para el usuario actual
            registros_despertar = Despertar.objects.filter(usuario_id=usuario_id)

            for despertar in registros_despertar:
                if despertar.fecha >= dormir.fecha:  # Considerar solo despertares posteriores
                    hora_dormir = datetime.combine(dormir.fecha, dormir.hora)
                    hora_despertar = datetime.combine(despertar.fecha, despertar.hora)

                    # Ajustar si el despertar es al día siguiente
                    if hora_despertar < hora_dormir:
                        hora_despertar += timedelta(days=1)

                    # Calcular el tiempo dormido
                    tiempo_dormido = (hora_despertar - hora_dormir).total_seconds()
                    item["total_horas"] += int(tiempo_dormido // 3600)
                    item["total_minutos"] += int((tiempo_dormido % 3600) // 60)
                    item["hora_despertar"] = despertar.hora.strftime("%H:%M:%S")
                    item["estado"] = despertar.estado

            usuario_info.append(item)

        # Devolver la respuesta paginada
        return self.get_paginated_response(usuario_info)
