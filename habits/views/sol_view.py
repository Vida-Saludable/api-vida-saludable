from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from users.models.usuario_models import Usuario

from ..models.sol_model import Sol
from ..serializers.sol_serializer import SolSerializer
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario

class CustomPagination(PageNumberPagination):
    page_size = 7  # Número de elementos por página
    page_size_query_param = 'page_size'  # Permite a los usuarios definir el tamaño de página en la solicitud
    max_page_size = 100  # Tamaño máximo de la página

class SolViewSet(viewsets.ModelViewSet):
    queryset = Sol.objects.all()
    serializer_class = SolSerializer
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        # Obtener el ID del usuario del cuerpo de la solicitud
        usuario_id = request.data.get('usuario')  # Asegúrate de que 'usuario' esté en el cuerpo de la solicitud

        # Verificar si el usuario existe
        try:
            usuario = Usuario.objects.get(id=usuario_id)  # Buscar el usuario por ID
        except Usuario.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Usuario no encontrado.'
            }, status=status.HTTP_404_NOT_FOUND)

        # Crear el serializer con los datos de la solicitud
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtener la fecha y verificar si ya existe un registro
        fecha = serializer.validated_data['fecha']  # Ajusta el campo según tu serializer
        registro_existente = Sol.objects.filter(fecha=fecha, usuario=usuario).first()

        if registro_existente:
            # Sumar el tiempo
            registro_existente.tiempo += serializer.validated_data['tiempo']  # Cambia 'tiempo' según tu modelo
            registro_existente.save()

            return Response({
                'success': True,
                'message': 'Tiempo actualizado exitosamente',
                'data': SolSerializer(registro_existente).data
            }, status=status.HTTP_200_OK)

        # Si no existe, crear el nuevo registro
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'success': True,
            'message': 'Registro exitoso',
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

        # Paginación
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data

            # Modificar los datos para agregar nombres_apellidos y telefono del usuario
            for item in data:
                usuario_id = item['usuario']  # Obtener el id del usuario
                datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()
                if datos_personales:
                    item['usuario'] = datos_personales.nombres_apellidos  # Reemplazar el ID con nombres_apellidos
                    item['telefono'] = datos_personales.telefono  # Agregar el telefono
                else:
                    item['usuario'] = None
                    item['telefono'] = None

            # Retornar la respuesta paginada con 'data'
            return Response({
                'success': True,
                'count': self.paginator.page.paginator.count,  # Total de elementos
                'next': self.paginator.get_next_link(),  # Enlace a la siguiente página
                'previous': self.paginator.get_previous_link(),  # Enlace a la página anterior
                'data': data  # Incluir los datos en 'data'
            }, status=status.HTTP_200_OK)

        # Si no hay paginación, serializar todos los elementos
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Modificar los datos para agregar nombres_apellidos y telefono del usuario
        for item in data:
            usuario_id = item['usuario']  # Obtener el id del usuario
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()
            if datos_personales:
                item['usuario'] = datos_personales.nombres_apellidos  # Reemplazar el ID con nombres_apellidos
                item['telefono'] = datos_personales.telefono  # Agregar el telefono
            else:
                item['usuario'] = None
                item['telefono'] = None

        return Response({
            'success': True,
            'message': 'Listado de registros de sol',
            'data': data  # Incluir los datos en 'data'
        }, status=status.HTTP_200_OK)
