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
        usuario = request.query_params.get('usuario', None)
        proyecto_id = request.query_params.get('proyecto', None)

        queryset = self.get_queryset().order_by('fecha')

        # Filtrar por usuario si existe parámetro
        if usuario:
            queryset = queryset.filter(usuario__datospersonalesusuario__nombres_apellidos__icontains=usuario)

        # Lógica para filtrar por proyecto
        if proyecto_id:
            if proyecto_id.lower() in ['all', 'todos']:
                # No filtrar, devolver todos los registros
                pass
            else:
                # Filtrar por proyecto específico
                queryset = queryset.filter(usuario__usuarioproyecto__proyecto__id=proyecto_id).distinct()
        else:
            # Si no hay parámetro, devolver solo los registros de usuarios que tengan proyecto relacionado
            queryset = queryset.filter(usuario__usuarioproyecto__isnull=False).distinct()

        paginated_queryset = self.paginate_queryset(queryset)

        usuario_info = []
        for esperanza in paginated_queryset:
            usuario_id = esperanza.usuario.id
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()

            usuario_info.append({
                "id": esperanza.id,
                "fecha": esperanza.fecha.strftime("%Y-%m-%d"),
                "usuario": datos_personales.nombres_apellidos if datos_personales else None,
                "telefono": datos_personales.telefono if datos_personales else None,
                "oracion": "oracion" if esperanza.tipo_practica == "oracion" else None,
                "leer_biblia": "leer biblia" if esperanza.tipo_practica == "leer biblia" else None,
            })

        page = self.paginator
        return Response({
            'success': True,
            'count': page.page.paginator.count,
            'next': page.get_next_link(),
            'previous': page.get_previous_link(),
            'data': usuario_info
        }, status=status.HTTP_200_OK)
