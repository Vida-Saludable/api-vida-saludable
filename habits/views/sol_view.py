from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from users.models.usuario_models import Usuario
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from users.models.usuario_proyecto_model import UsuarioProyecto

from ..models.sol_model import Sol
from ..serializers.sol_serializer import SolSerializer

class CustomPagination(PageNumberPagination):
    page_size = 7
    page_size_query_param = 'page_size'
    max_page_size = 100

class SolViewSet(viewsets.ModelViewSet):
    queryset = Sol.objects.all()
    serializer_class = SolSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Obtener el ID del usuario del cuerpo de la solicitud
        usuario_id = request.data.get('usuario')

        # Verificar si el usuario existe
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Usuario no encontrado.'
            }, status=status.HTTP_404_NOT_FOUND)

        # Crear el serializer con los datos de la solicitud
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtener la fecha y verificar si ya existe un registro
        fecha = serializer.validated_data['fecha']
        registro_existente = Sol.objects.filter(fecha=fecha, usuario=usuario).first()

        if registro_existente:
            # Sumar el tiempo
            registro_existente.tiempo += serializer.validated_data['tiempo']
            registro_existente.save()

            # Obtener proyectos del usuario para la respuesta
            proyectos_usuario = UsuarioProyecto.objects.filter(usuario=usuario).values_list('proyecto__nombre', flat=True)
            
            response_data = SolSerializer(registro_existente).data
            response_data['proyectos_usuario'] = list(proyectos_usuario)

            return Response({
                'success': True,
                'message': 'Tiempo actualizado exitosamente',
                'data': response_data
            }, status=status.HTTP_200_OK)

        # Si no existe, crear el nuevo registro
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Obtener proyectos del usuario para la respuesta
        proyectos_usuario = UsuarioProyecto.objects.filter(usuario_id=usuario_id).values_list('proyecto__nombre', flat=True)
        response_data = serializer.data
        response_data['proyectos_usuario'] = list(proyectos_usuario)

        return Response({
            'success': True,
            'message': 'Registro exitoso',
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

        # Filtrar por usuario si existe parámetro
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
            'message': 'Listado de registros de sol',
            'data': data
        }, status=status.HTTP_200_OK)