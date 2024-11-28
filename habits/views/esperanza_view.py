from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from ..models.esperanza_model import Esperanza
from ..serializers.esperanza_serializer import EsperanzaSerializer
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario


class CustomPagination(PageNumberPagination):
    page_size = 7  # Número de elementos por página
    page_size_query_param = 'page_size'  # Permite a los usuarios definir el tamaño de página en la solicitud
    max_page_size = 100  # Tamaño máximo de la página


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

        # Aplicar paginación
        page = self.paginate_queryset(queryset)
        if page is not None:
            processed_data = self._process_queryset(page)
            return self.get_paginated_response(processed_data)

        # Procesar datos si no hay paginación
        data = self._process_queryset(queryset)
        return Response({
            'success': True,
            'message': 'Listado de registros de esperanza',
            'data': data
        }, status=status.HTTP_200_OK)

    def _process_queryset(self, queryset):
        """Procesa el queryset en el formato deseado."""
        usuario_info = {}

        for esperanza in queryset:
            usuario_id = esperanza.usuario.id
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()

            # Agrupar por fecha
            fecha_str = esperanza.fecha.strftime("%Y-%m-%d")
            if fecha_str not in usuario_info:
                usuario_info[fecha_str] = {
                    "fecha": fecha_str,
                    "usuario": datos_personales.nombres_apellidos if datos_personales else None,
                    "telefono": datos_personales.telefono if datos_personales else None,
                    "oracion": None,
                    "leer_biblia": None,
                    "id": esperanza.id,  # Añadir ID del registro
                }

            # Asignar el tipo de práctica
            if esperanza.tipo_practica == "oracion":
                usuario_info[fecha_str]["oracion"] = esperanza.tipo_practica
            elif esperanza.tipo_practica == "leer biblia":
                usuario_info[fecha_str]["leer_biblia"] = esperanza.tipo_practica

        # Convertir el diccionario a lista
        return list(usuario_info.values())
