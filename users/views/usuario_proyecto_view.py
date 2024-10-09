from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models.usuario_models import Usuario
from users.models.usuario_proyecto_model import UsuarioProyecto
from users.serializers.proyecto_serializer import ProyectoSerializer
from users.serializers.usuario_proyecto_serializer import UsuarioProyectoSerializer

class UsuarioProyectoViewSet(viewsets.ModelViewSet):
    queryset = UsuarioProyecto.objects.all()
    serializer_class = UsuarioProyectoSerializer
    # permission_classes = [IsAuthenticated]

class ListaProyectosPorUsuarioView(APIView):
    
    def get(self, request, usuario_id):
        try:
            # Verificar que el usuario exista
            usuario = Usuario.objects.get(id=usuario_id)

            # Obtener los proyectos asociados al usuario mediante la relación UsuarioProyecto
            usuario_proyectos = UsuarioProyecto.objects.filter(usuario=usuario)

            if not usuario_proyectos.exists():
                return Response(
                    {"message": "Este usuario no tiene proyectos asociados."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Extraer los proyectos relacionados con el usuario
            proyectos = [usuario_proyecto.proyecto for usuario_proyecto in usuario_proyectos]

            # Serializar los proyectos
            serializer = ProyectoSerializer(proyectos, many=True)
            
            # Filtrar solo los campos deseados (id, nombre y descripcion) y agrupar en 'data'
            proyectos_filtrados = [
                {
                    "id": proyecto["id"],  # Incluir el ID del proyecto
                    "nombre": proyecto["nombre"],
                    "descripcion": proyecto["descripcion"]
                } for proyecto in serializer.data
            ]
            
            # Crear la respuesta final con 'success', 'message' y 'data' (proyectos)
            response_data = {
                "success": True,
                "message": "Proyectos obtenidos exitosamente.",
                "data": proyectos_filtrados  # Proyectos dentro de 'data'
            }
            
            # Devolver la respuesta en formato JSON
            return Response(response_data, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )