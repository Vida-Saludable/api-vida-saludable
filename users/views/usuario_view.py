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

            # 2. Registrar UsuarioProyecto (requiere el ID del usuario y varios proyectos)
            proyectos_ids = request.data.get('proyectos_ids', [])  # Obtener la lista de IDs de proyectos
            
            # Verificar si se enviaron proyectos
            if not proyectos_ids:
                return Response({
                    'success': False,
                    'message': 'Debe seleccionar al menos un proyecto.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Asociar al usuario con cada proyecto
            usuario_proyecto_data = []
            for proyecto_id in proyectos_ids:
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

            # 1. Actualizar los datos del Usuario (sin contraseña)
            usuario_serializer = self.get_serializer(usuario, data=request.data, partial=True)
            usuario_serializer.is_valid(raise_exception=True)
            usuario_serializer.save()  # Se actualiza el usuario

            # 2. Actualizar o crear las relaciones UsuarioProyecto
            proyectos_ids = request.data.get('proyectos_ids', [])
            
            if proyectos_ids:
                # Eliminar relaciones anteriores
                UsuarioProyecto.objects.filter(usuario=usuario).delete()
                
                # Crear nuevas relaciones para cada proyecto
                for proyecto_id in proyectos_ids:
                    usuario_proyecto_data = {'usuario': usuario.id, 'proyecto': proyecto_id}
                    usuario_proyecto_serializer = UsuarioProyectoSerializer(data=usuario_proyecto_data)
                    usuario_proyecto_serializer.is_valid(raise_exception=True)
                    usuario_proyecto_serializer.save()

            # Respuesta de éxito si todo se actualizó correctamente
            return Response({
                'success': True,
                'message': 'Usuario actualizado correctamente',
                'data': {
                    'usuario': usuario_serializer.data,
                    'proyectos': proyectos_ids  # Devolver los proyectos actualizados
                }
            }, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            return Response({'success': False, 'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


        
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response({
    #         "success": True,
    #         "message": "Usuario eliminado correctamente"
    #     }, status=status.HTTP_200_OK)

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
            # Obtener los proyectos asociados al usuario
            usuario_proyectos = UsuarioProyecto.objects.filter(usuario=usuario)
            nombres_proyectos = [proyecto.proyecto.nombre for proyecto in usuario_proyectos] if usuario_proyectos else []

            # Serializar los datos del usuario
            usuario_serializado = UsuarioSerializer(usuario).data

            # Construir los datos del usuario
            usuario_info = {
                'id': usuario.id,  # Incluimos el ID del usuario
                'nombre': usuario_serializado.get('nombre'),  # Nombre del usuario
                'correo': usuario_serializado.get('correo'),  # Correo electrónico del usuario
                'role': usuario.role.name if usuario.role else None,  # Obtener el nombre del rol
                'proyectos': nombres_proyectos  # Incluir los nombres de los proyectos asociados
            }

            usuarios_data.append(usuario_info)

        return Response(usuarios_data)

