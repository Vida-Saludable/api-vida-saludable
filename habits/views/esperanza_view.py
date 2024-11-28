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

    def get_paginated_response(self, data):
        """Personaliza la estructura de la respuesta paginada."""
        return Response({
            'success': True,
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data
        })


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
        usuario = request.query_params.get('usuario', None)
        proyecto_id = request.query_params.get('proyecto', None)

        queryset = self.get_queryset().order_by('fecha')

        if usuario:
            queryset = queryset.filter(usuario__datospersonalesusuario__nombres_apellidos__icontains=usuario)

        if proyecto_id:
            queryset = queryset.filter(usuario__usuarioproyecto__proyecto__id=proyecto_id).distinct()

        page = self.paginate_queryset(queryset)
        if page is not None:
            processed_data = self._process_queryset(page)
            return self.get_paginated_response(processed_data)

        data = self._process_queryset(queryset)
        return Response({
            'success': True,
            'count': len(data),
            'next': None,
            'previous': None,
            'data': data
        }, status=status.HTTP_200_OK)

    def _process_queryset(self, queryset):
        """Procesa el queryset en el formato deseado."""
        usuario_info = {}

        for esperanza in queryset:
            usuario_id = esperanza.usuario.id
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()

            fecha_str = esperanza.fecha.strftime("%Y-%m-%d")
            if fecha_str not in usuario_info:
                usuario_info[fecha_str] = {
                    "fecha": fecha_str,
                    "usuario": datos_personales.nombres_apellidos if datos_personales else None,
                    "telefono": datos_personales.telefono if datos_personales else None,
                    "oracion": None,
                    "leer_biblia": None,
                    "id": esperanza.id,  # ID agregado aquí
                }

            if esperanza.tipo_practica == "oracion":
                usuario_info[fecha_str]["oracion"] = esperanza.tipo_practica
            elif esperanza.tipo_practica == "leer biblia":
                usuario_info[fecha_str]["leer_biblia"] = esperanza.tipo_practica

        return list(usuario_info.values())
