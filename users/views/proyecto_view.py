from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models.proyecto_model import Proyecto
from users.models.usuario_models import Usuario
from users.models.usuario_proyecto_model import UsuarioProyecto
from users.serializers.proyecto_serializer import ProyectoSerializer
from users.serializers.usuario_serializer import UsuarioSerializer
class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "success": True,
            "message": "Proyecto registrado correctamente",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "success": True,
            "message": "Proyecto actualizado correctamente",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        instance = serializer.save()
        estado = serializer.validated_data.get('estado')
        if estado is not None:
            instance.estado = estado
        instance.save()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "success": True,
            "message": "Proyecto eliminado correctamente"
        }, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()

# class ListaProyectoUsuariosView(APIView):
#     def get(self, request, usuario_id):
#         try:
#             # Verificar que el usuario exista
#             usuario = Usuario.objects.get(id=usuario_id)

#             # Obtener los proyectos asociados al usuario mediante la relación UsuarioProyecto
#             usuario_proyectos = UsuarioProyecto.objects.filter(usuario=usuario)

#             if not usuario_proyectos.exists():
#                 return Response(
#                     {"message": "Este usuario no tiene proyectos asociados."},
#                     status=status.HTTP_404_NOT_FOUND
#                 )
            
#             # Extraer los proyectos relacionados con el usuario
#             proyectos = [usuario_proyecto.proyecto for usuario_proyecto in usuario_proyectos]

#             # Serializar los proyectos
#             serializer = ProyectoSerializer(proyectos, many=True)
            
#             # Filtrar solo los campos deseados (id, nombre y descripcion) y agrupar en 'data'
#             proyectos_filtrados = [
#                 {
#                     "id": proyecto["id"],  # Incluir el ID del proyecto
#                     "nombre": proyecto["nombre"],
#                     "descripcion": proyecto["descripcion"]
#                 } for proyecto in serializer.data
#             ]
            
#             # Crear la respuesta final con 'success', 'message' y 'data' (proyectos)
#             response_data = {
#                 "success": True,
#                 "message": "Proyectos obtenidos exitosamente.",
#                 "data": proyectos_filtrados  # Proyectos dentro de 'data'
#             }
            
#             # Devolver la respuesta en formato JSON
#             return Response(response_data, status=status.HTTP_200_OK)

#         except Usuario.DoesNotExist:
#             return Response(
#                 {"error": "Usuario no encontrado"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
