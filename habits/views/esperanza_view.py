from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from ..models.esperanza_model import Esperanza
from ..serializers.esperanza_serializer import EsperanzaSerializer
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario


class CustomPagination(PageNumberPagination):
    page_size = 7  # Número de elementos por página
    page_size_query_param = 'page_size'
    max_page_size = 100


class EsperanzaViewSet(viewsets.ModelViewSet):
    queryset = Esperanza.objects.all()
    serializer_class = EsperanzaSerializer
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
        for esperanza in paginated_queryset:
            usuario_id = esperanza.usuario.id
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()

            # Construir el objeto final por cada registro
            usuario_info.append({
                "id": esperanza.id,
                "fecha": esperanza.fecha.strftime("%Y-%m-%d"),
                "usuario": datos_personales.nombres_apellidos if datos_personales else None,
                "telefono": datos_personales.telefono if datos_personales else None,
                "oracion": "oracion" if esperanza.tipo_practica == "oracion" else None,
                "leer_biblia": "leer biblia" if esperanza.tipo_practica == "leer biblia" else None,
            })

        # Devolver los datos paginados en la respuesta
        return self.get_paginated_response(usuario_info)