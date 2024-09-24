from rest_framework import viewsets, generics
from django.db import transaction
from rest_framework.pagination import PageNumberPagination

from users.models.proyecto_model import Proyecto
from users.models.role_model import Role
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

            # 2. Registrar UsuarioProyecto (requiere el ID del usuario y varios proyectos)
            proyectos = request.data.get('proyectos', [])  # Obtener la lista de IDs de proyectos
            
            # Verificar si se enviaron proyectos
            if not proyectos:
                return Response({
                    'success': False,
                    'message': 'Debe seleccionar al menos un proyecto.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Asociar al usuario con cada proyecto
            usuario_proyecto_data = []
            for proyecto_id in proyectos:
                usuario_proyecto_data.append({
                    'usuario': usuario.id,
                    'proyecto': proyecto_id
                })

            # Guardar las asociaciones
            for data in usuario_proyecto_data:
                usuario_proyecto_serializer = UsuarioProyectoSerializer(data=data)
                usuario_proyecto_serializer.is_valid(raise_exception=True)
                usuario_proyecto_serializer.save()

            # Respuesta de éxito si todo se guardó correctamente
            return Response({
                'success': True,
                'message': 'Usuario registrado correctamente',
                'data': {
                    'usuario': usuario_serializer.data,
                    'usuario_proyectos': usuario_proyecto_data  # Devuelve la lista de asociaciones
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Si hay algún error, se deshacen todas las operaciones
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        try:
            # Obtener el usuario que se va a actualizar
            usuario_id = kwargs.get('pk')  # ID del usuario pasado en la URL
            usuario = Usuario.objects.get(id=usuario_id)

            # Filtrar solo los campos permitidos para la actualización
            allowed_fields = ['nombre', 'correo', 'role']  # Campos que se pueden editar
            filtered_data = {field: request.data[field] for field in allowed_fields if field in request.data}

            # Actualizar los datos del Usuario (solo los campos permitidos)
            usuario_serializer = self.get_serializer(usuario, data=filtered_data, partial=True)
            usuario_serializer.is_valid(raise_exception=True)
            usuario_serializer.save()  # Se actualiza el usuario

            # Respuesta de éxito si todo se actualizó correctamente
            return Response({
                'success': True,
                'message': 'Usuario actualizado correctamente',
                'data': usuario_serializer.data  # Devolver los datos del usuario actualizado
            }, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            return Response({'success': False, 'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class RegistroUsuarioView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListaUsuariosView(APIView):
    def get(self, request, *args, **kwargs):
        # Filtrar todos los usuarios que no tengan el rol 'Paciente'
        usuarios = Usuario.objects.exclude(role__name="Paciente")
        usuarios_data = []

        for usuario in usuarios:
            # Serializar los datos del usuario
            usuario_serializado = UsuarioSerializer(usuario).data
            
            # Obtener todos los proyectos asociados al usuario mediante la tabla intermedia UsuarioProyecto
            usuario_proyectos = UsuarioProyecto.objects.filter(usuario=usuario)
            proyectos_data = [{'id': up.proyecto.id, 'nombre': up.proyecto.nombre} for up in usuario_proyectos]

            # Armar la respuesta con la información del usuario y sus proyectos
            usuario_info = {
                'id': usuario.id,
                'nombre': usuario_serializado.get('nombre'),
                'correo': usuario_serializado.get('correo'),
                'role': usuario.role.name if usuario.role else None,
                'proyectos': proyectos_data  # Añadir la lista de proyectos asociados
            }

            usuarios_data.append(usuario_info)

        return Response(usuarios_data, status=200)

class ListaPacientesView(APIView):
    def get(self, request, *args, **kwargs):
        # Filtrar todos los usuarios que tengan el rol 'Paciente'
        pacientes = Usuario.objects.filter(role__name="Paciente")

        # Lista de usuarios con los datos requeridos
        pacientes_data = []

        for paciente in pacientes:
            # Serializar los datos del usuario
            paciente_serializado = UsuarioSerializer(paciente).data

            # Obtener el proyecto asociado al paciente
            usuario_proyectos = UsuarioProyecto.objects.filter(usuario=paciente)

            # Obtener solo los nombres de los proyectos
            proyectos_nombres = [usuario_proyecto.proyecto.nombre for usuario_proyecto in usuario_proyectos]

            paciente_info = {
                'id': paciente.id,  # Incluimos el ID del usuario
                'nombre': paciente_serializado.get('nombre'),  # Nombre del usuario
                'correo': paciente_serializado.get('correo'),  # Correo electrónico del usuario
                'role': paciente.role.name if paciente.role else None,  # Obtener el nombre del rol
                'proyectos': proyectos_nombres  # Agregar solo los nombres de los proyectos
            }

            pacientes_data.append(paciente_info)

        # Crear la respuesta final con éxito y mensaje
        response_data = {
            'success': True,
            'message': 'Lista de pacientes obtenida con éxito.',
            'data': pacientes_data
        }

        return Response(response_data, status=200)

