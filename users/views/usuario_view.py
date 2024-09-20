from rest_framework import viewsets, generics
from django.db import transaction
from rest_framework.pagination import PageNumberPagination

from users.models.usuario_models import Usuario
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from users.models.usuario_proyecto_model import UsuarioProyecto
# from users.models.role_model import Role

from users.serializers.usuario_serializer import UsuarioSerializer
from users.serializers.datos_personales_serializers import DatosPersonalesUsuarioSerializer
from users.serializers.usuario_proyecto_serializer import UsuarioProyectoSerializer
from users.serializers.proyecto_serializer import ProyectoSerializer


from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10 

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            # 1. Registrar el Usuario
            usuario_serializer = self.get_serializer(data=request.data)
            usuario_serializer.is_valid(raise_exception=True)
            usuario = usuario_serializer.save()  # Guarda el usuario y obtiene el ID

            # 2. Registrar DatosPersonalesUsuario (requiere el ID del usuario registrado)
            # Obtener los datos personales directamente desde el cuerpo de la solicitud
            datos_personales = {
                'nombres_apellidos': request.data.get('nombres_apellidos'),
                'telefono': request.data.get('telefono'),
                'usuario': usuario.id  # Asignar el ID del usuario recién creado
            }
            datos_personales_serializer = DatosPersonalesUsuarioSerializer(data=datos_personales)
            datos_personales_serializer.is_valid(raise_exception=True)
            datos_personales_usuario = datos_personales_serializer.save()

            # 3. Registrar UsuarioProyecto (requiere el ID del usuario y del proyecto)
            proyecto_id = request.data.get('proyecto_id')
            usuario_proyecto_data = {
                'usuario': usuario.id,
                'proyecto': proyecto_id
            }
            usuario_proyecto_serializer = UsuarioProyectoSerializer(data=usuario_proyecto_data)
            usuario_proyecto_serializer.is_valid(raise_exception=True)
            usuario_proyecto_serializer.save()

            # Respuesta de éxito si todo se guardó correctamente
            return Response({
                'success': True,
                'message': 'Usuario registrado correctamente',
                'data': {
                    'usuario': usuario_serializer.data,
                    'datos_personales': datos_personales_serializer.data,
                    'usuario_proyecto': usuario_proyecto_serializer.data
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Si hay algún error, se deshacen todas las operaciones
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "success": True,
            "message": "Usuario eliminado correctamente"
        }, status=status.HTTP_200_OK)

class RegistroUsuarioView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListaUsuariosView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener todos los usuarios
        usuarios = Usuario.objects.all()

        # Lista de usuarios con los datos requeridos
        usuarios_data = []

        for usuario in usuarios:
            # Obtener los datos personales del usuario
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario=usuario).first()

            # Obtener el proyecto asociado al usuario
            usuario_proyecto = UsuarioProyecto.objects.filter(usuario=usuario).first()
            nombre_proyecto = usuario_proyecto.proyecto.nombre if usuario_proyecto else None

            # Serializar los datos
            usuario_serializado = UsuarioSerializer(usuario).data
            datos_personales_serializado = DatosPersonalesUsuarioSerializer(datos_personales).data if datos_personales else {}

            # Construir los datos del usuario
            usuario_info = {
                'id': usuario.id,  # Incluimos el ID del usuario
                'nombres_apellidos': datos_personales_serializado.get('nombres_apellidos'),
                'correo': usuario_serializado.get('correo'),
                'role': usuario.role.name if usuario.role else None,  # Obtener el nombre del rol
                'proyecto_id': nombre_proyecto,  # Incluir el nombre del proyecto
                'telefono': datos_personales_serializado.get('telefono')
            }

            usuarios_data.append(usuario_info)

        return Response(usuarios_data)