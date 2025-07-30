from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from ..models.ejercicio_model import Ejercicio
from ..serializers.ejercicio_serializer import EjercicioSerializer
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario

class CustomPagination(PageNumberPagination):
    page_size = 7  # Número de elementos por página
    page_size_query_param = 'page_size'  # Permite a los usuarios definir el tamaño de página en la solicitud
    max_page_size = 100  # Tamaño máximo de la página
class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer
    pagination_class = CustomPagination
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
        usuario = request.query_params.get('usuario', None)
        proyecto_id = request.query_params.get('proyecto', None)

        queryset = self.get_queryset().order_by('fecha')

        # Filtrar por usuario
        if usuario:
            queryset = queryset.filter(usuario__datospersonalesusuario__nombres_apellidos__icontains=usuario)

        # Filtrar por proyecto según condición
        if proyecto_id:
            if proyecto_id.lower() in ['all', 'todos']:
                # No filtrar por proyecto, mostrar todos
                pass
            else:
                queryset = queryset.filter(usuario__usuarioproyecto__proyecto__id=proyecto_id).distinct()
        else:
            # Sin parámetro proyecto, solo usuarios con proyectos relacionados
            queryset = queryset.filter(usuario__usuarioproyecto__isnull=False).distinct()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data

            # Reemplazar id usuario con nombres y agregar teléfono
            for item in data:
                usuario_id = item['usuario']
                datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()
                if datos_personales:
                    item['usuario'] = datos_personales.nombres_apellidos
                    item['telefono'] = datos_personales.telefono
                else:
                    item['usuario'] = None
                    item['telefono'] = None

            return Response({
                'success': True,
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'data': data
            }, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        for item in data:
            usuario_id = item['usuario']
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()
            if datos_personales:
                item['usuario'] = datos_personales.nombres_apellidos
                item['telefono'] = datos_personales.telefono
            else:
                item['usuario'] = None
                item['telefono'] = None

        return Response({
            'success': True,
            'message': 'Listado de registros de ejercicio',
            'data': data
        }, status=status.HTTP_200_OK)
