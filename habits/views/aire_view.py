from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from ..models.aire_model import Aire
from ..serializers.aire_serializer import AireSerializer
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from users.models.usuario_proyecto_model import UsuarioProyecto

class CustomPagination(PageNumberPagination):
    page_size = 7
    page_size_query_param = 'page_size'
    max_page_size = 100

class AireViewSet(viewsets.ModelViewSet):
    queryset = Aire.objects.all()
    serializer_class = AireSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Obtener proyectos del usuario para la respuesta
        usuario_id = request.data.get('usuario')
        proyectos_usuario = UsuarioProyecto.objects.filter(usuario_id=usuario_id).values_list('proyecto__nombre', flat=True)
        
        response_data = serializer.data
        response_data['proyectos_usuario'] = list(proyectos_usuario)
        
        headers = self.get_success_headers(serializer.data)
        return Response({
            'success': True,
            'message': 'Se registró exitosamente',
            'data': response_data
        }, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        usuario = request.query_params.get('usuario', None)
        proyecto_id = request.query_params.get('proyecto', None)
        usuario_autenticado = request.user

        # Obtener proyectos del usuario autenticado
        proyectos_usuario = UsuarioProyecto.objects.filter(usuario=usuario_autenticado).values_list('proyecto_id', flat=True)
        
        queryset = self.get_queryset().order_by('fecha')
        
        # Filtrar solo registros de usuarios que estén en los proyectos del usuario autenticado
        queryset = queryset.filter(usuario__usuarioproyecto__proyecto_id__in=proyectos_usuario).distinct()

        # Filtrar por nombre de usuario si se especifica
        if usuario:
            queryset = queryset.filter(usuario__datospersonalesusuario__nombres_apellidos__icontains=usuario)

        # Filtrar por proyecto específico si se indica
        if proyecto_id and proyecto_id.lower() not in ['all', 'todos']:
            queryset = queryset.filter(usuario__usuarioproyecto__proyecto__id=proyecto_id).distinct()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data

            for item in data:
                usuario_id = item['usuario']
                datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()
                proyectos = UsuarioProyecto.objects.filter(usuario_id=usuario_id).values_list('proyecto__nombre', flat=True)
                
                if datos_personales:
                    item['usuario'] = datos_personales.nombres_apellidos
                    item['telefono'] = datos_personales.telefono
                else:
                    item['usuario'] = None
                    item['telefono'] = None
                
                item['proyectos_usuario'] = list(proyectos)

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
            proyectos = UsuarioProyecto.objects.filter(usuario_id=usuario_id).values_list('proyecto__nombre', flat=True)
            
            if datos_personales:
                item['usuario'] = datos_personales.nombres_apellidos
                item['telefono'] = datos_personales.telefono
            else:
                item['usuario'] = None
                item['telefono'] = None
            
            item['proyectos_usuario'] = list(proyectos)

        return Response({
            'success': True,
            'message': 'Listado de registros de aire',
            'data': data
        }, status=status.HTTP_200_OK)