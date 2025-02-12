from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.models.usuario_models import Usuario
from users.models.usuario_proyecto_model import UsuarioProyecto
from users.serializers.proyecto_serializer import ProyectoSerializer
from users.serializers.usuario_proyecto_serializer import UsuarioProyectoSerializer

class UsuarioProyectoViewSet(viewsets.ModelViewSet):
    queryset = UsuarioProyecto.objects.all()
    serializer_class = UsuarioProyectoSerializer
    

    def create(self, request, *args, **kwargs):
        # Crear el nuevo registro
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Preparar la respuesta con el formato solicitado
        response_data = {
            "success": True,
            "message": "Registro creado exitosamente.",
            "data": serializer.data  # Los datos del nuevo registro creado
        }
        
        # Devolver la respuesta con los datos del nuevo registro
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        # Obtener el objeto a eliminar
        try:
            instance = self.get_object()
            self.perform_destroy(instance)

            # Preparar la respuesta exitosa
            response_data = {
                "success": True,
                "message": "Registro eliminado exitosamente.",
                "data": {
                    "id": instance.id,
                    "usuario": instance.usuario.id,  # ID del usuario relacionado
                    "proyecto": instance.proyecto.id  # ID del proyecto relacionado
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except UsuarioProyecto.DoesNotExist:
            # Si no se encuentra el registro
            return Response(
                {"success": False, "message": "Registro no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

    def perform_destroy(self, instance):
        # Método que realiza la eliminación real del registro
        instance.delete()

class ListaProyectosPorUsuarioView(APIView):

    
    def get(self, request, usuario_id):
        try:
            # Verificar que el usuario existe
            usuario = Usuario.objects.get(id=usuario_id)

            # Obtener los registros de UsuarioProyecto asociados a este usuario
            usuario_proyectos = UsuarioProyecto.objects.filter(usuario=usuario)

            if not usuario_proyectos.exists():
                return Response(
                    {"message": "Este usuario no tiene proyectos asignados."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Obtener los proyectos de cada registro de UsuarioProyecto
            proyectos = [usuario_proyecto.proyecto for usuario_proyecto in usuario_proyectos]

            # Serializar los proyectos, obteniendo solo nombre y descripcion
            proyectos_filtrados = [
                {
                    "id": usuario_proyecto.id,  # ID del registro en UsuarioProyecto
                    "nombre": proyecto.nombre,
                    "descripcion": proyecto.descripcion
                } for usuario_proyecto, proyecto in zip(usuario_proyectos, proyectos)
            ]

            # Crear la respuesta final
            response_data = {
                "success": True,
                "message": "Proyectos obtenidos exitosamente.",
                "data": proyectos_filtrados
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )